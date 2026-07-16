#!/usr/bin/env python3
"""
Download all images from ikropka.eu via WordPress REST API
More reliable than web scraping
"""

import requests
import os
import time
from pathlib import Path
from urllib.parse import urlparse

API_BASE = "https://ikropka.eu/wp-json/wp/v2/media"
OUTPUT_DIR = Path(__file__).parent.parent / "scraped-content" / "images" / "original"

def download_image(url, filename):
    """Download a single image"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        filepath = OUTPUT_DIR / filename

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"  ERROR downloading {filename}: {e}")
        return False

def main():
    print("Downloading images via WordPress REST API...")
    print(f"Output: {OUTPUT_DIR}")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    page = 1
    total_downloaded = 0
    total_skipped = 0

    while True:
        print(f"Fetching page {page}...")

        try:
            response = requests.get(f"{API_BASE}?per_page=100&page={page}", timeout=30)
            response.raise_for_status()
            media_items = response.json()
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

        # Check if no more items
        if not media_items or len(media_items) == 0:
            print("No more pages. Done!")
            break

        for item in media_items:
            source_url = item.get('source_url')
            if not source_url:
                continue

            # Get filename from URL
            filename = os.path.basename(urlparse(source_url).path)

            # Skip if already exists
            if (OUTPUT_DIR / filename).exists():
                print(f"  Skip: {filename} (exists)")
                total_skipped += 1
                continue

            # Download
            print(f"  Downloading: {filename}")
            if download_image(source_url, filename):
                total_downloaded += 1

        page += 1

        # Be polite - wait between pages
        time.sleep(1)

    # Final count
    final_count = len(list(OUTPUT_DIR.glob('*')))

    print()
    print("=" * 40)
    print("Download Complete")
    print("=" * 40)
    print(f"Downloaded: {total_downloaded}")
    print(f"Skipped (already exist): {total_skipped}")
    print(f"Total files in directory: {final_count}")
    print(f"Output: {OUTPUT_DIR}")
    print()
    print("Next steps:")
    print("  1. Deduplicate: node scripts/deduplicate-wp-thumbnails.js")
    print("  2. Optimize: ./scripts/optimize-images.sh")

if __name__ == "__main__":
    main()
