import json
from typing import List, Dict


def load_data(filename: str) -> Dict[str, str]:
    """
        Load data from a JSON file.

        Args:
            - filename: The name of the JSON file to load data from.

        Returns:
            - A dictionary containing the loaded data.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data


def save_data(data: List[Dict[str, str]], filename: str) -> None:
    """
        Save data to a JSON file.

        Args:
            - data: The data to be saved to the JSON file.
            - filename: The name of the JSON file to save data to.
    """
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
