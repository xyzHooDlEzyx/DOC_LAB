import json
import urllib.request
from typing import Dict, List


class HttpJsonFetcher:
    def fetch(self, url: str) -> List[Dict[str, object]]:
        with urllib.request.urlopen(url) as response:
            payload = response.read().decode("utf-8")
        data = json.loads(payload)
        if not isinstance(data, list):
            raise ValueError("Expected JSON array from dataset.")
        return data
