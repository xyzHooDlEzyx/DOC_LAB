from abc import ABC, abstractmethod


class IInsuranceDataImporter(ABC):
    @abstractmethod
    def import_from_csv(self, file_path: str) -> dict:
        raise NotImplementedError
