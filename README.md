# Multi-Threaded Data Scraper

> Efficiently download images or files in bulk using configurable task queues and CSV-driven batch scheduling — with built-in folder structure handling, rate limiting, and retry logic.

---

### ⚠️ IMPORTANT

This tool enables you to efficiently — and in many cases, *over-efficiently* — make multiple requests per time interval.

**It is your responsibility to verify and respect the rate limits imposed by the servers you are requesting data from.**  

---

## Features

- Modular architecture with clear separation of concerns
- CSV-driven: list URLs, categories, and IDs in simple CSVs
- Multi-threaded downloader (with concurrency control)
- Structured folder output (`flat`, `by_date`, or `per-CSV`)
- Supports multiple CSVs in one batch run
- MIT licensed — use freely

---

## Getting Started

### Installation

Clone the repository:

```bash
git clone https://github.com/Devon-du-Toit/Multi-Thread-Data-Scraper.git
cd DataScraper
pip install -r requirements.txt
```

## Configuration

Edit `config.json` to set your preferences:

```
  "output_root": Output data folder
  "csv_file_list": list (min 1) of files to download from
  "url_column": column in csv to request data from
  "max_downloads": number of rows in csv file to request for data
  "download_structure": "flat", "by_date", "by_source"
  "timeout": Wait time for request responses
  "retry_attempts": ammount of attempts before failure on a request
  "concurrent_workers": Parallel threads to run (CHECK RATE LIMITS OF SERVERS)
  "log_level": set logger visibility
```

---

## CSV Format

Your CSV files must contain a column with a unique `id` and a column with image/file URLs.

```csv
id,image_url,date
001,https://example.com/image1.jpg,2025-07-18
002,https://example.com/image2.jpg,2025-07-18
```

- `id`: used for filenames
- `image_url`: your URL column (configure via `url_column`)
- `date`: optional, used for structured folders

---

## Running the Downloader

```bash
python collector.py
```

Each CSV in your list will be processed one by one, with its own timestamped output folder.

---

## Logging

- Logs are written to `logs/collector.log`
- Real-time progress is shown in the terminal

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.

---
