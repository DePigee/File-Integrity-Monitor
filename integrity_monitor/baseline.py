import json


def save_baseline(data: dict[str, str], file_path: str) -> None:
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)


def load_baseline(file_path: str) -> dict[str, str]:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Baseline file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Baseline file is corrupted: {file_path}")

    if not isinstance(data, dict):
        raise ValueError(f"Baseline file has the wrong format: {file_path}")
    return data