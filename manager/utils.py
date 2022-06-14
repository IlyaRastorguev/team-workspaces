from typing import Dict

import yaml


def load_yaml(file_name: str) -> Dict:
    with open(file_name, "r") as f:
        data = yaml.safe_load(f)
    return data
