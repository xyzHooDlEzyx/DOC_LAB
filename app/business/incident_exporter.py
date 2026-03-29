from typing import Dict

from ..data_access.http_json_fetcher import HttpJsonFetcher
from ..data_access.json_file_reader import JsonFileReader
from ..data_access.json_file_writer import JsonFileWriter
from .output_strategies import OutputStrategy


class IncidentExporter:
    def __init__(
        self,
        fetcher: HttpJsonFetcher,
        writer: JsonFileWriter,
        reader: JsonFileReader,
        output: OutputStrategy,
    ) -> None:
        self._fetcher = fetcher
        self._writer = writer
        self._reader = reader
        self._output = output

    def export(self, url: str, output_file: str) -> Dict[str, int]:
        records = self._fetcher.fetch(url)
        saved = self._writer.write(output_file, records)
        file_records = self._reader.read(output_file)
        output_count = self._output.write_records(file_records)
        return {
            "downloaded": len(records),
            "saved": saved,
            "output": output_count,
        }
