from abc import ABC, abstractmethod


class IInsurancePresentation(ABC):
    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError
