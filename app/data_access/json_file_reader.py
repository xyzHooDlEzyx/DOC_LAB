import json
from typing import Dict, Iterable, List


class JsonFileReader:
    def read(self, file_path: str) -> Iterable[Dict[str, object]]:
        with open(file_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("Expected JSON array in file.")
        return data
