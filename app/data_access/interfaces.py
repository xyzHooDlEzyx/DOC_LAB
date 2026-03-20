from abc import ABC, abstractmethod
from typing import Dict, Iterable, List


class ICsvReader(ABC):
    @abstractmethod
    def read_rows(self, file_path: str) -> Iterable[Dict[str, str]]:
        raise NotImplementedError


class IDataWriter(ABC):
    @abstractmethod
    def save_models(
        self,
        agents,
        customers,
        destinations,
        policies,
    ) -> None:
        raise NotImplementedError


class IPolicyRepository(ABC):
    @abstractmethod
    def list_policies(self):
        raise NotImplementedError

    @abstractmethod
    def get_policy(self, policy_id: int):
        raise NotImplementedError

    @abstractmethod
    def list_agents(self):
        raise NotImplementedError

    @abstractmethod
    def list_customers(self):
        raise NotImplementedError

    @abstractmethod
    def list_destinations(self):
        raise NotImplementedError

    @abstractmethod
    def get_agent(self, agent_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_customer(self, customer_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_destinations_by_ids(self, destination_ids: List[int]):
        raise NotImplementedError

    @abstractmethod
    def add_policy(self, policy) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_policy(self, policy) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_policy(self, policy) -> None:
        raise NotImplementedError


class ICustomerRepository(ABC):
    @abstractmethod
    def list_customers(self):
        raise NotImplementedError

    @abstractmethod
    def get_customer(self, customer_id: int):
        raise NotImplementedError

    @abstractmethod
    def add_customer(self, customer) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_customer(self, customer) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_customer(self, customer) -> None:
        raise NotImplementedError
