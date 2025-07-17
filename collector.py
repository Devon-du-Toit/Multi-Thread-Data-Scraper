import os
from tqdm import tqdm
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from utils.config import load_config
from utils.logger import get_logger
from utils.downloader import download_file
from utils.file_utils import ensure_dir_exists
from queue_manager import load_tasks

logger = get_logger()


def process_csv(csv_path: str, config: dict):
    logger.info(f"Processing CSV file: {csv_path}")

    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    csv_output_root = os.path.join(config["output_root"], f"{timestamp}_{base_name}")

    tasks = load_tasks(
        csv_path,
        csv_output_root,
        config["download_structure"],
        config["max_downloads"],
        config["url_column"]
    )

    for task in tasks:
        ensure_dir_exists(task["output_dir"])

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    csv_output_root = os.path.join(config["output_root"], f"{timestamp}_{base_name}")

    tasks = load_tasks(
        csv_path,
        csv_output_root,
        config["download_structure"],
        config["max_downloads"],
        config["url_column"]
    )

    for task in tasks:
        ensure_dir_exists(task["output_dir"])

    progress_bar = tqdm(total=len(tasks), desc=base_name, unit="file")

    def download_and_track(task):
        result = download_file(
            task,
            task["output_dir"],
            config["timeout"],
            config["retry_attempts"]
        )
        progress_bar.update(1)
        return result

    with ThreadPoolExecutor(max_workers=config["concurrent_workers"]) as executor:
        futures = [executor.submit(download_and_track, task) for task in tasks]
        for future in futures:
            future.result()

    progress_bar.close()
    logger.info(f"Finished processing CSV: {csv_path}")


def main():
    config = load_config()
    print("Loading Config completed...")

    csv_files = config.get("csv_file_list", [])
    print(f"CSV files to process: {csv_files}")

    if not csv_files:
        logger.warning("No matching CSV files found.")
        print("No matching CSV files found.")
        return

    for csv_file in csv_files:
        try:
            process_csv(csv_file, config)
            logger.info(f"Finished processing {csv_file}")
        except Exception as e:
            logger.error(f"Error processing {csv_file}: {e}")


if __name__ == "__main__":
    main()
