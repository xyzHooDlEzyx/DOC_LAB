from datetime import datetime
import uuid

from .interfaces import IPolicyService
from ..data_access.interfaces import IPolicyRepository
from ..models import InsurancePolicy


class PolicyService(IPolicyService):
    def __init__(self, repository: IPolicyRepository) -> None:
        self._repository = repository

    def list_policies(self, order: str = "asc"):
        normalized = (order or "asc").lower()
        if normalized not in {"asc", "desc"}:
            normalized = "asc"
        return self._repository.list_policies(normalized)

    def get_policy(self, policy_id: int):
        policy = self._repository.get_policy(policy_id)
        if policy is None:
            raise ValueError("Policy not found")
        return policy

    def get_form_options(self) -> dict:
        return {
            "agents": self._repository.list_agents(),
            "customers": self._repository.list_customers(),
            "destinations": self._repository.list_destinations(),
        }

    def create_policy(self, payload: dict) -> None:
        coverage_start = self._parse_date(payload["coverage_start"])
        coverage_end = self._parse_date(payload["coverage_end"])
        policy = InsurancePolicy(
            policy_identifier=self._generate_policy_identifier(),
            base_premium=float(payload["base_premium"]),
            final_price=0,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            trip_type=self._normalize_trip_type(payload.get("trip_type")),
            is_family=self._parse_bool(payload.get("is_family")),
            family_size=self._parse_family_size(payload.get("family_size")),
        )
        self._validate_family_size(policy.is_family, policy.family_size)
        self._apply_relations(policy, payload)
        policy.final_price = self._calculate_final_price(
            policy.base_premium,
            coverage_start,
            coverage_end,
            policy.destinations,
            policy.customer.health_state,
            policy.trip_type,
            policy.is_family,
            policy.family_size,
            policy.agent.specialization,
        )
        self._repository.add_policy(policy)

    def update_policy(self, policy_id: int, payload: dict) -> None:
        policy = self.get_policy(policy_id)
        coverage_start = self._parse_date(payload["coverage_start"])
        coverage_end = self._parse_date(payload["coverage_end"])
        policy.base_premium = float(payload["base_premium"])
        policy.coverage_start = coverage_start
        policy.coverage_end = coverage_end
        policy.trip_type = self._normalize_trip_type(payload.get("trip_type"))
        policy.is_family = self._parse_bool(payload.get("is_family"))
        policy.family_size = self._parse_family_size(payload.get("family_size"))
        self._validate_family_size(policy.is_family, policy.family_size)
        self._apply_relations(policy, payload)
        policy.final_price = self._calculate_final_price(
            policy.base_premium,
            coverage_start,
            coverage_end,
            policy.destinations,
            policy.customer.health_state,
            policy.trip_type,
            policy.is_family,
            policy.family_size,
            policy.agent.specialization,
        )
        self._repository.update_policy(policy)

    def delete_policy(self, policy_id: int) -> None:
        policy = self.get_policy(policy_id)
        self._repository.delete_policy(policy)

    def _apply_relations(self, policy: InsurancePolicy, payload: dict) -> None:
        agent_id = int(payload["agent_id"])
        customer_id = int(payload["customer_id"])
        destination_ids = [int(value) for value in payload.get("destinations", [])]

        agent = self._repository.get_agent(agent_id)
        if agent is None:
            raise ValueError("Agent not found")
        if not self._is_agent_allowed(agent.specialization, policy.trip_type, policy.is_family):
            raise ValueError("Agent specialization is not allowed for this policy")
        customer = self._repository.get_customer(customer_id)
        if customer is None:
            raise ValueError("Customer not found")

        destinations = self._repository.get_destinations_by_ids(destination_ids)
        policy.agent = agent
        policy.customer = customer
        policy.destinations = destinations

    @staticmethod
    def _calculate_final_price(
        base_premium: float,
        coverage_start,
        coverage_end,
        destinations,
        health_state: str,
        trip_type: str,
        is_family: bool,
        family_size: int,
        agent_specialization: str,
    ) -> float:
        if coverage_end < coverage_start:
            raise ValueError("Coverage end must be on or after start date")
        duration_days = (coverage_end - coverage_start).days + 1
        risk_multiplier = 1.0
        for destination in destinations:
            risk_multiplier = max(
                risk_multiplier,
                PolicyService._map_risk_level(destination.risk_level),
            )
        base_value = base_premium + (duration_days * risk_multiplier)
        if len(destinations) > 1:
            base_value *= 1.20
        if PolicyService._is_bad_health(health_state):
            base_value += 2.0
        base_value *= PolicyService._trip_type_multiplier(trip_type)
        if PolicyService._is_premium_agent(agent_specialization):
            base_value *= 1.20
        if is_family:
            base_value += (base_premium * 0.10)
            base_value += 20.0 * max(family_size, 1)
        return round(base_value, 2)

    @staticmethod
    def _map_risk_level(value: str) -> float:
        normalized = value.strip().lower()
        mapping = {
            "low": 1.0,
            "medium": 1.5,
            "high": 2.0,
        }
        if normalized not in mapping:
            raise ValueError("Unknown risk level")
        return mapping[normalized]

    @staticmethod
    def _normalize_trip_type(value: str) -> str:
        normalized = (value or "").strip().lower()
        return normalized if normalized in {"business", "leisure", "adventure", "study"} else "leisure"

    @staticmethod
    def _trip_type_multiplier(value: str) -> float:
        normalized = (value or "").strip().lower()
        mapping = {
            "business": 1.10,
            "leisure": 1.00,
            "adventure": 1.20,
            "study": 1.00,
        }
        return mapping.get(normalized, 1.00)

    @staticmethod
    def _parse_bool(value: str) -> bool:
        return (value or "").strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def _parse_family_size(value: str) -> int:
        try:
            size = int(value)
        except (TypeError, ValueError):
            size = 1
        return max(size, 1)

    @staticmethod
    def _validate_family_size(is_family: bool, family_size: int) -> None:
        if is_family and family_size < 2:
            raise ValueError("Family size must be at least 2")

    @staticmethod
    def _allowed_specializations(trip_type: str, is_family: bool):
        normalized = (trip_type or "").strip().lower()
        mapping = {
            "business": {"business", "premium"},
            "leisure": {"adventure", "premium"},
            "adventure": {"adventure", "premium"},
            "study": {"student", "premium"},
        }
        allowed = set(mapping.get(normalized, {"premium"}))
        if is_family:
            allowed.add("family")
        return allowed

    @staticmethod
    def _is_agent_allowed(specialization: str, trip_type: str, is_family: bool) -> bool:
        normalized = (specialization or "").strip().lower()
        return normalized in PolicyService._allowed_specializations(trip_type, is_family)

    @staticmethod
    def _is_premium_agent(specialization: str) -> bool:
        return (specialization or "").strip().lower() == "premium"

    @staticmethod
    def _is_bad_health(value: str) -> bool:
        if not value:
            return False
        normalized = value.strip().lower()
        return normalized in {"bad", "risk"}

    @staticmethod
    def _parse_date(value: str):
        return datetime.strptime(value, "%Y-%m-%d").date()

    @staticmethod
    def _generate_policy_identifier() -> str:
        return f"P{uuid.uuid4().hex[:8].upper()}"
