import json
from typing import List, Dict

OUTPUT_FILENAME = 'manufacturers_data.json'


def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data


def save_data(data: List[Dict[str, str]], filename: str) -> None:
    """
    Save combined data to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
