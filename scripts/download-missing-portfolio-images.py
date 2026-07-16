#!/usr/bin/env python3
"""
Download missing portfolio images from live ikropka.eu site.

For each portfolio post:
1. Extract all image references from frontmatter (featured_image + gallery)
2. Try to download from ikropka.eu (checking multiple date paths)
3. Save to docs/assets/images/portfolio/{slug}/
"""

import os
import re
import yaml
import requests
from pathlib import Path
from urllib.parse import urlparse
import time

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
PORTFOLIO_DIR = DOCS_DIR / "_portfolio"
PORTFOLIO_IMAGES = DOCS_DIR / "assets/images/portfolio"

# Base URLs to try (WordPress often reorganizes uploads by date)
BASE_URLS = [
    "https://ikropka.eu/wp-content/uploads/2023/03/",
    "https://ikropka.eu/wp-content/uploads/2022/06/",
    "https://ikropka.eu/wp-content/uploads/2022/",
    "https://ikropka.eu/wp-content/uploads/2021/",
    "https://ikropka.eu/wp-content/uploads/2023/",
    "https://ikropka.eu/wp-content/uploads/2020/",
]

def extract_frontmatter_and_content(md_file):
    """Extract YAML frontmatter and markdown content separately."""
    content = md_file.read_text(encoding='utf-8')

    if not content.startswith('---\n'):
        return None, content

    parts = content.split('\n---\n', 1)
    if len(parts) != 2:
        return None, content

    yaml_text = parts[0][4:]  # Remove opening ---\n
    markdown_content = parts[1]

    try:
        frontmatter = yaml.safe_load(yaml_text)
        return frontmatter, markdown_content
    except yaml.YAMLError as e:
        print(f"   ⚠️  YAML parse error in {md_file.name}: {e}")
        return None, content

def download_image(filename, target_path):
    """
    Try to download image from ikropka.eu, checking multiple date paths.
    Returns True if successful, False otherwise.
    """
    if target_path.exists():
        print(f"      ⏭️  Already exists: {filename}")
        return True

    # Try each base URL
    for base_url in BASE_URLS:
        url = base_url + filename

        try:
            response = requests.get(url, timeout=10, allow_redirects=True)

            if response.status_code == 200:
                # Check if it's actually an image (not HTML error page)
                content_type = response.headers.get('Content-Type', '')
                if 'image' in content_type or filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    # Save to file
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_bytes(response.content)

                    # Get file size
                    size_kb = len(response.content) / 1024
                    print(f"      ✓ Downloaded: {filename} ({size_kb:.1f} KB) from {base_url}")
                    return True
        except requests.RequestException:
            continue

    print(f"      ✗ Not found: {filename}")
    return False

def process_portfolio_post(md_file):
    """Process a single portfolio markdown file."""
    slug = md_file.stem
    print(f"\n📄 {slug}")

    # Parse frontmatter
    frontmatter, markdown_content = extract_frontmatter_and_content(md_file)

    if frontmatter is None:
        print(f"   ⚠️  Skipping (no valid frontmatter)")
        return

    # Create target directory for images
    target_dir = PORTFOLIO_IMAGES / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    # Collect all images to download
    images_to_download = []

    # Add featured_image
    if 'featured_image' in frontmatter and frontmatter['featured_image']:
        path = frontmatter['featured_image']
        filename = Path(path).name
        images_to_download.append(filename)

    # Add gallery images
    if 'gallery' in frontmatter and isinstance(frontmatter['gallery'], list):
        for gallery_item in frontmatter['gallery']:
            if isinstance(gallery_item, dict) and 'image' in gallery_item:
                path = gallery_item['image']
                filename = Path(path).name
                images_to_download.append(filename)

    # Remove duplicates
    images_to_download = list(set(images_to_download))

    if not images_to_download:
        print(f"   ⏭️  No images to download")
        return

    print(f"   📊 Found {len(images_to_download)} images")

    # Download each image
    downloaded = 0
    for filename in images_to_download:
        target_path = target_dir / filename
        if download_image(filename, target_path):
            downloaded += 1

        # Rate limit to be nice to the server
        time.sleep(0.2)

    print(f"   ✅ Downloaded {downloaded}/{len(images_to_download)} images")

def main():
    """Main entry point."""
    print("=" * 70)
    print("🌐  DOWNLOAD MISSING PORTFOLIO IMAGES FROM ikropka.eu")
    print("=" * 70)

    if not PORTFOLIO_DIR.exists():
        print(f"❌ Portfolio directory not found: {PORTFOLIO_DIR}")
        return

    # Get all portfolio posts
    portfolio_posts = sorted(PORTFOLIO_DIR.glob("*.md"))
    print(f"\n📚 Found {len(portfolio_posts)} portfolio posts\n")

    total_posts = 0
    total_downloaded = 0

    for md_file in portfolio_posts:
        try:
            # Count images before
            slug = md_file.stem
            target_dir = PORTFOLIO_IMAGES / slug
            before_count = len(list(target_dir.glob("*"))) if target_dir.exists() else 0

            process_portfolio_post(md_file)

            # Count images after
            after_count = len(list(target_dir.glob("*"))) if target_dir.exists() else 0
            new_images = after_count - before_count
            total_downloaded += new_images

            total_posts += 1
        except Exception as e:
            print(f"\n❌ Error processing {md_file.name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print(f"✅ COMPLETE")
    print("=" * 70)
    print(f"Posts processed:  {total_posts}/{len(portfolio_posts)}")
    print(f"Images downloaded: {total_downloaded}")
    print("=" * 70)

    # Show summary of folders
    if PORTFOLIO_IMAGES.exists():
        folders_with_images = []
        folders_empty = []

        for folder in sorted(PORTFOLIO_IMAGES.iterdir()):
            if folder.is_dir():
                image_count = len(list(folder.glob("*")))
                if image_count > 0:
                    folders_with_images.append((folder.name, image_count))
                else:
                    folders_empty.append(folder.name)

        print(f"\n📁 Folders with images: {len(folders_with_images)}")

        if folders_empty:
            print(f"\n⚠️  Folders still empty: {len(folders_empty)}")
            if len(folders_empty) <= 10:
                for folder in folders_empty:
                    print(f"   - {folder}")

if __name__ == "__main__":
    main()
