from .business.importer import InsuranceDataImporter
from .business.customer_service import CustomerService
from .business.policy_service import PolicyService
from .data_access.csv_reader import CsvDataReader
from .data_access.db_writer import SqlAlchemyDataWriter
from .data_access.customer_repository import SqlAlchemyCustomerRepository
from .data_access.policy_repository import SqlAlchemyPolicyRepository


def build_importer() -> InsuranceDataImporter:
    return InsuranceDataImporter(CsvDataReader(), SqlAlchemyDataWriter())


def build_policy_service() -> PolicyService:
    return PolicyService(SqlAlchemyPolicyRepository())


def build_customer_service() -> CustomerService:
    return CustomerService(SqlAlchemyCustomerRepository())
