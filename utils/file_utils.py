import os
from datetime import date

def ensure_dir_exists(path: str):
    os.makedirs(path, exist_ok=True)

def build_output_path(base: str, structure: str, row: dict) -> str:
    if structure == "flat":
        return base  # no extra folders
    elif structure == "by_date":
        return os.path.join(base, row["category"], row["date"])
    elif structure == "by_source":
        return os.path.join(base, row["category"])
    elif structure == "by_current_date":
        today_str = date.today().isoformat()
        return os.path.join(base, today_str)
    else:
        return base
