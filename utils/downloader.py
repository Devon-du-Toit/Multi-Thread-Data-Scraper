import requests
import os
from utils.logger import get_logger

logger = get_logger()


def download_file(task, output_dir, timeout=10, retries=3):
    url = task['url']
    filename = task['filename']
    filepath = os.path.join(output_dir, filename)

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
            logger.info(f"Downloaded: {filepath}")
            return filepath
        except Exception as e:
            logger.warning(f"Retry {attempt + 1} for {url} failed: {e}")
    logger.error(f"Failed to download: {url}")
    return None
