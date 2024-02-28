import json
import logging as logger


def save_file(data: dict, file_path: str):
    try:
        with open(file=file_path, mode="w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.warn(f"Can not save file at {file_path} with exception {e}")
