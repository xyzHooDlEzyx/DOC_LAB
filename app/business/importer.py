from datetime import datetime
from typing import Dict

from .interfaces import IInsuranceDataImporter
from ..data_access.interfaces import ICsvReader, IDataWriter
from ..models import Customer, Destination, InsuranceAgent, InsurancePolicy


class InsuranceDataImporter(IInsuranceDataImporter):
    def __init__(self, reader: ICsvReader, writer: IDataWriter) -> None:
        self._reader = reader
        self._writer = writer

    def import_from_csv(self, file_path: str) -> Dict[str, int]:
        agents_by_id = {}
        customers_by_id = {}
        destinations_by_country = {}
        policies_by_id = {}
        policy_destination_cache = {}

        for row in self._reader.read_rows(file_path):
            agent_id = row["agent_id"].strip()
            customer_id = row["customer_id"].strip()
            policy_id = row["policy_id"].strip()
            country = row["destination_country"].strip()

            agent = agents_by_id.get(agent_id)
            if agent is None:
                agent = InsuranceAgent(
                    agent_identifier=agent_id,
                    specialization=row["agent_specialization"].strip(),
                )
                agents_by_id[agent_id] = agent

            customer = customers_by_id.get(customer_id)
            if customer is None:
                customer = Customer(
                    customer_identifier=customer_id,
                    full_name=row["customer_name"].strip(),
                    age=int(row["customer_age"]),
                    health_state=row["customer_health_state"].strip(),
                    gender=row.get("customer_gender", "").strip() or None,
                    health_condition=row.get("customer_health_condition", "").strip()
                    or None,
                )
                customers_by_id[customer_id] = customer

            destination = destinations_by_country.get(country)
            if destination is None:
                destination = Destination(
                    country=country,
                    risk_level=row["destination_risk_level"].strip(),
                )
                destinations_by_country[country] = destination

            policy = policies_by_id.get(policy_id)
            if policy is None:
                policy = InsurancePolicy(
                    policy_identifier=policy_id,
                    base_premium=float(row["base_premium"]),
                    final_price=float(row["final_price"]),
                    coverage_start=datetime.strptime(
                        row["coverage_start"], "%Y-%m-%d"
                    ).date(),
                    coverage_end=datetime.strptime(
                        row["coverage_end"], "%Y-%m-%d"
                    ).date(),
                    trip_type=row.get("trip_type", "leisure").strip() or "leisure",
                    is_family=(row.get("is_family", "").strip().lower() == "true"),
                    family_size=int(row.get("family_size", "1")),
                    agent=agent,
                    customer=customer,
                )
                policies_by_id[policy_id] = policy
                policy_destination_cache[policy_id] = set()

            cached_destinations = policy_destination_cache[policy_id]
            if country not in cached_destinations:
                policy.destinations.append(destination)
                cached_destinations.add(country)

        self._writer.save_models(
            list(agents_by_id.values()),
            list(customers_by_id.values()),
            list(destinations_by_country.values()),
            list(policies_by_id.values()),
        )

        return {
            "agents": len(agents_by_id),
            "customers": len(customers_by_id),
            "destinations": len(destinations_by_country),
            "policies": len(policies_by_id),
        }
