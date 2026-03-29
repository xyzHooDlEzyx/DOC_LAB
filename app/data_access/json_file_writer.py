import json
import os
from typing import Iterable, Mapping


class JsonFileWriter:
    def write(self, file_path: str, records: Iterable[Mapping[str, object]]) -> int:
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        records_list = list(records)
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(records_list, handle, ensure_ascii=True, indent=2)
        return len(records_list)
