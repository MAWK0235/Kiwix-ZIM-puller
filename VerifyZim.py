import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def get_zim_links(url):
    """Fetch all .zim file links from the provided URL."""
    try:
        print(f"Fetching content from: {url}")
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return [
        urljoin(url, link['href'])
        for link in soup.find_all('a', href=True)
        if link['href'].endswith('.zim')
    ]

def get_remote_file_size(url):
    """Perform a HEAD request to get Content-Length (file size)."""
    try:
        head_resp = requests.head(url, allow_redirects=True)
        head_resp.raise_for_status()
        return int(head_resp.headers.get('Content-Length', 0))
    except Exception as e:
        print(f"⚠️  Failed to get size for {url}: {e}")
        return None

def download_file(url, output_path):
    """Download a file from a URL to a specific path."""
    try:
        if "survivorlibrary" in url:
            print(f"⏭️  Skipping {url} (contains 'survivorlibrary')")
            return

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('Content-Length', 0))
            downloaded_size = 0

            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\r⬇️  Downloading {os.path.basename(output_path)}: {progress:.2f}%", end="")

        print(f"\n✅ Downloaded {os.path.basename(output_path)}")
    except Exception as e:
        print(f"\n❌ Failed to download {url}: {e}")

def verify_and_redownload(url, download_dir="./"):
    zim_links = get_zim_links(url)
    if not zim_links:
        print("No .zim files found.")
        return

    print(f"\n🔍 Found {len(zim_links)} .zim files to verify.\n")
    for zim_url in zim_links:
        original_file_name = os.path.basename(urlparse(zim_url).path)
        cleaned_file_name = original_file_name.removeprefix("openZIM_")
        local_path = os.path.join(download_dir, cleaned_file_name)

        remote_size = get_remote_file_size(zim_url)
        if remote_size is None:
            print(f"⚠️  Skipping {cleaned_file_name}: could not determine remote size.")
            continue

        # Check if file exists and is complete
        if os.path.exists(local_path):
            local_size = os.path.getsize(local_path)
            if local_size == remote_size:
                print(f"✅ OK: {cleaned_file_name}")
                continue
            else:
                print(f"❌ INCOMPLETE: {cleaned_file_name} (local: {local_size}, remote: {remote_size}) — Redownloading...")
                os.remove(local_path)
        else:
            print(f"❌ MISSING: {cleaned_file_name} — Downloading...")

        # Download the file
        download_file(zim_url, local_path)

    print("\n✅ Verification and re-download process completed.")

if __name__ == "__main__":
    target_url = "https://premium-preppers.demo.hotspot.kiwix.org/download/"
    verify_and_redownload(target_url)
