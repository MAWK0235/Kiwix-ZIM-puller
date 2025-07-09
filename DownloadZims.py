import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def download_zim_files(url, download_dir="./"):
    """
    Downloads all .zim files found on a given URL, removing 'openZIM_' prefix from filenames.

    Args:
        url (str): The URL of the webpage to scrape for .zim files.
        download_dir (str): The directory where the .zim files will be saved.
    """
    try:
        print(f"Fetching content from: {url}")
        response = requests.get(url, stream=True, allow_redirects=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    base_url = urlparse(url).scheme + "://" + urlparse(url).netloc

    zim_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.zim'):
            full_url = urljoin(url, href)
            zim_links.append(full_url)

    if not zim_links:
        print("No .zim files found on the page.")
        return

    print(f"Found {len(zim_links)} .zim files. Starting download...")

    for zim_url in zim_links:
        original_file_name = os.path.basename(urlparse(zim_url).path)
        # Remove "openZIM_" prefix if present
        cleaned_file_name = original_file_name.removeprefix("openZIM_")

        file_path = os.path.join(download_dir, cleaned_file_name)

        # Skip if file with cleaned name already exists
        if os.path.exists(file_path):
            print(f"Skipping {cleaned_file_name}: File already exists in {download_dir}")
            continue

        print(f"Downloading {cleaned_file_name} from {zim_url}")
        try:
            with requests.get(zim_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                downloaded_size = 0
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"\rDownloading {cleaned_file_name}: {progress:.2f}%", end="")
            print(f"\nSuccessfully downloaded {cleaned_file_name}")
        except requests.exceptions.RequestException as e:
            print(f"\nError downloading {cleaned_file_name}: {e}")
        except IOError as e:
            print(f"\nError saving {cleaned_file_name} to disk: {e}")

if __name__ == "__main__":
    target_url = "https://premium-preppers.demo.hotspot.kiwix.org/download/"
    download_zim_files(target_url)
    print("\nDownload process completed.")
