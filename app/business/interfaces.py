from abc import ABC, abstractmethod


class IInsuranceDataImporter(ABC):
    @abstractmethod
    def import_from_csv(self, file_path: str) -> dict:
        raise NotImplementedError


class IPolicyService(ABC):
    @abstractmethod
    def list_policies(self):
        raise NotImplementedError

    @abstractmethod
    def get_policy(self, policy_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_form_options(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_policy(self, payload: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_policy(self, policy_id: int, payload: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_policy(self, policy_id: int) -> None:
        raise NotImplementedError


class ICustomerService(ABC):
    @abstractmethod
    def list_customers(self):
        raise NotImplementedError

    @abstractmethod
    def get_customer(self, customer_id: int):
        raise NotImplementedError

    @abstractmethod
    def create_customer(self, payload: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_customer(self, customer_id: int, payload: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_customer(self, customer_id: int) -> None:
        raise NotImplementedError
