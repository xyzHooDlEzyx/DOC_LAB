import uuid

from .interfaces import ICustomerService
from ..data_access.interfaces import ICustomerRepository
from ..models import Customer


class CustomerService(ICustomerService):
    def __init__(self, repository: ICustomerRepository) -> None:
        self._repository = repository

    def list_customers(self):
        return self._repository.list_customers()

    def get_customer(self, customer_id: int):
        customer = self._repository.get_customer(customer_id)
        if customer is None:
            raise ValueError("Customer not found")
        return customer

    def create_customer(self, payload: dict) -> None:
        customer = Customer(
            customer_identifier=self._generate_customer_identifier(),
            full_name=self._required(payload, "full_name"),
            age=self._parse_age(payload.get("age")),
            health_state=self._required(payload, "health_state"),
            gender=self._optional(payload, "gender"),
            health_condition=self._optional(payload, "health_condition"),
        )
        self._repository.add_customer(customer)

    def update_customer(self, customer_id: int, payload: dict) -> None:
        customer = self.get_customer(customer_id)
        customer.full_name = self._required(payload, "full_name")
        customer.age = self._parse_age(payload.get("age"))
        customer.health_state = self._required(payload, "health_state")
        customer.gender = self._optional(payload, "gender")
        customer.health_condition = self._optional(payload, "health_condition")
        self._repository.update_customer(customer)

    def delete_customer(self, customer_id: int) -> None:
        customer = self.get_customer(customer_id)
        self._repository.delete_customer(customer)

    @staticmethod
    def _required(payload: dict, key: str) -> str:
        value = payload.get(key, "").strip()
        if not value:
            raise ValueError(f"{key.replace('_', ' ').title()} is required")
        return value

    @staticmethod
    def _optional(payload: dict, key: str):
        value = payload.get(key, "").strip()
        return value or None

    @staticmethod
    def _parse_age(value: str) -> int:
        try:
            age = int(value)
        except (TypeError, ValueError):
            raise ValueError("Age must be a number")
        if age <= 0:
            raise ValueError("Age must be positive")
        return age

    @staticmethod
    def _generate_customer_identifier() -> str:
        return f"C{uuid.uuid4().hex[:8].upper()}"
