import csv
from typing import Dict, Iterable

from .interfaces import ICsvReader


class CsvDataReader(ICsvReader):
    def read_rows(self, file_path: str) -> Iterable[Dict[str, str]]:
        with open(file_path, "r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                yield row
