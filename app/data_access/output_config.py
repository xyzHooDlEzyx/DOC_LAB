import json
import os
from typing import Dict


def load_incident_config(config_path: str) -> Dict[str, object]:
    with open(config_path, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    return _resolve_paths(config, config_path)


def _resolve_paths(config: Dict[str, object], config_path: str) -> Dict[str, object]:
    dataset = config.get("dataset", {})
    output_file = dataset.get("output_file", "")
    if output_file and not os.path.isabs(output_file):
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(config_path), "..", "..")
        )
        dataset["output_file"] = os.path.abspath(
            os.path.join(base_dir, output_file)
        )
    config["dataset"] = dataset
    return config
