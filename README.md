# 📚 ZIM File Downloader & Verifier

This repository provides two Python scripts to **download** and **verify** `.zim` files from a web page (specifically tested with [Kiwix's preppers library](https://premium-preppers.demo.hotspot.kiwix.org/download/)).

- `verify_and_redownload.py`: Verifies existing files and redownloads missing or incomplete `.zim` files.
- `download_zim_files.py`: Downloads all `.zim` files that are not already present.

## ✅ Features

- Automatically fetches `.zim` file links from a webpage.
- Skips URLs containing `survivorlibrary`.
- Verifies file size before skipping or redownloading.
- Cleans up filenames by removing the `openZIM_` prefix.
- Shows real-time download progress.
- Uses streaming to avoid memory overload on large files.

---

## 📦 Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`

Install dependencies via pip:

```bash
pip install -r requirements.txt
