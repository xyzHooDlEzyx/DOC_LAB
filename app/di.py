from .business.importer import InsuranceDataImporter
from .data_access.csv_reader import CsvDataReader
from .data_access.db_writer import SqlAlchemyDataWriter


def build_importer() -> InsuranceDataImporter:
    return InsuranceDataImporter(CsvDataReader(), SqlAlchemyDataWriter())
