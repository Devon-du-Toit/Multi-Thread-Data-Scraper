import csv
import os
from urllib.parse import urlparse, urljoin
from typing import List, Dict
from utils.file_utils import build_output_path

def get_file_extension(url):
    parsed = urlparse(url)
    return os.path.splitext(parsed.path)[-1]

def load_tasks(
    csv_path: str,
    output_root: str,
    structure: str,
    url_prefix: str,
    url_suffix: str,
    id_column: str,
    max_tasks: int = None,
    url_column: str = "source_url",
    delimiter: str = ","
) -> List[Dict]:
    """
    Loads tasks from a CSV and returns a list of download task dicts.
    """
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]
        tasks = []
        for i, row in enumerate(reader):
            if max_tasks is not None and i >= max_tasks:
                break

            url_value = row.get(url_column, "").strip()
            if not url_value:
                print(f"Skipping row {i}: missing value in column '{url_column}'")
                continue

            url = url_value

            if url_prefix:
                url = urljoin(url_prefix.rstrip('/') + '/', url.lstrip('/'))

            if url_suffix:
                url = urljoin(url.rstrip('/') + '/', url_suffix.lstrip('/'))

            file_ext = get_file_extension(url) or ".jpg"
            id_value = row.get(id_column, "").strip()
            if not id_value:
                print(f"Skipping row {i}: missing value in column '{id_column}'")
                continue

            filename = f"{id_value}{file_ext}"

            output_dir = build_output_path(output_root, structure, row)

            task = {
                "id": id_value,
                "url": url,
                "category": row.get("category", ""),
                "date": row.get("date", ""),
                "filename": filename,
                "output_dir": output_dir
            }
            tasks.append(task)

    return tasks
