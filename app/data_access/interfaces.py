from abc import ABC, abstractmethod
from typing import Dict, Iterable


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
