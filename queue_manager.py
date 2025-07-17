import csv
import os
from urllib.parse import urlparse
from typing import List, Dict
from utils.file_utils import build_output_path

def get_file_extension(url):
    parsed = urlparse(url)
    return os.path.splitext(parsed.path)[-1]

def load_tasks(
    csv_path: str,
    output_root: str,
    structure: str,
    max_tasks: int = None,
    url_column: str = "source_url"
) -> List[Dict]:
    """
    Loads tasks from a CSV and returns a list of download task dicts.
    """
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        tasks = []
        for i, row in enumerate(reader):
            if max_tasks is not None and i >= max_tasks:
                break

            # Extract URL and extension dynamically
            url = row[url_column]
            file_ext = get_file_extension(url) or ".bin"
            filename = f"{row['id']}{file_ext}"
            output_dir = build_output_path(output_root, structure, row)

            task = {
                "id": row["id"],
                "url": url,
                "category": row.get("category", ""),
                "date": row.get("date", ""),
                "filename": filename,
                "output_dir": output_dir
            }
            tasks.append(task)

    return tasks
