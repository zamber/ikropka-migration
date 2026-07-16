#!/usr/bin/env python3
"""
Organize portfolio images into proper folder structure.

For each portfolio post:
1. Extract slug from filename
2. Create docs/assets/images/portfolio/{slug}/ folder
3. Find all images referenced in frontmatter (featured_image + gallery)
4. Copy them from scraped-content/images/original/ to the portfolio folder
5. Update image paths in frontmatter to match new structure
"""

import os
import re
import shutil
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
PORTFOLIO_DIR = DOCS_DIR / "_portfolio"
SCRAPED_IMAGES = PROJECT_ROOT / "scraped-content/images/original"
PORTFOLIO_IMAGES = DOCS_DIR / "assets/images/portfolio"

# Build index of available scraped images (case-insensitive)
print("📸 Building image index from scraped content...")
scraped_images_map = {}
for img_file in SCRAPED_IMAGES.glob("*"):
    if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        # Store both exact name and lowercase version for matching
        scraped_images_map[img_file.name.lower()] = img_file

print(f"   Found {len(scraped_images_map)} images in scraped-content/")

def extract_frontmatter_and_content(md_file):
    """Extract YAML frontmatter and markdown content separately."""
    content = md_file.read_text(encoding='utf-8')

    if not content.startswith('---\n'):
        return None, content

    # Split on closing ---
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

def find_and_copy_image(image_path_or_filename, target_dir, slug):
    """
    Find image in scraped content and copy to target directory.
    Returns new path if successful, None otherwise.
    """
    # Extract just the filename from path
    if '/' in image_path_or_filename:
        filename = Path(image_path_or_filename).name
    else:
        filename = image_path_or_filename

    # Try case-insensitive match
    filename_lower = filename.lower()

    if filename_lower in scraped_images_map:
        source_file = scraped_images_map[filename_lower]
        target_file = target_dir / source_file.name

        # Copy if not already there
        if not target_file.exists():
            shutil.copy2(source_file, target_file)
            print(f"      ✓ Copied: {source_file.name}")

        # Return new path
        return f"/assets/images/portfolio/{slug}/{source_file.name}"
    else:
        print(f"      ✗ Not found: {filename}")
        return None

def process_portfolio_post(md_file):
    """Process a single portfolio markdown file."""
    # Extract slug from filename
    slug = md_file.stem

    print(f"\n📄 Processing: {slug}")

    # Parse frontmatter
    frontmatter, markdown_content = extract_frontmatter_and_content(md_file)

    if frontmatter is None:
        print(f"   ⚠️  Skipping (no valid frontmatter)")
        return

    # Create target directory for images
    target_dir = PORTFOLIO_IMAGES / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    # Track if anything changed
    changed = False
    images_processed = 0
    images_found = 0

    # Process featured_image
    if 'featured_image' in frontmatter and frontmatter['featured_image']:
        old_path = frontmatter['featured_image']
        new_path = find_and_copy_image(old_path, target_dir, slug)
        if new_path:
            frontmatter['featured_image'] = new_path
            changed = True
            images_found += 1
        images_processed += 1

    # Process gallery images
    if 'gallery' in frontmatter and isinstance(frontmatter['gallery'], list):
        for i, gallery_item in enumerate(frontmatter['gallery']):
            if isinstance(gallery_item, dict) and 'image' in gallery_item:
                old_path = gallery_item['image']
                new_path = find_and_copy_image(old_path, target_dir, slug)
                if new_path:
                    frontmatter['gallery'][i]['image'] = new_path
                    changed = True
                    images_found += 1
                images_processed += 1

    print(f"   📊 Images: {images_found}/{images_processed} found and copied")

    # Write back if changed
    if changed:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            f.write("---\n")
            f.write(markdown_content)
        print(f"   ✅ Updated: {md_file.name}")
    else:
        print(f"   ⏭️  No changes needed")

def main():
    """Main entry point."""
    print("=" * 60)
    print("🖼️  PORTFOLIO IMAGE ORGANIZER")
    print("=" * 60)

    if not PORTFOLIO_DIR.exists():
        print(f"❌ Portfolio directory not found: {PORTFOLIO_DIR}")
        return

    if not SCRAPED_IMAGES.exists():
        print(f"❌ Scraped images directory not found: {SCRAPED_IMAGES}")
        return

    # Get all portfolio posts
    portfolio_posts = list(PORTFOLIO_DIR.glob("*.md"))
    print(f"\n📚 Found {len(portfolio_posts)} portfolio posts")

    # Process each post
    total_processed = 0
    for md_file in sorted(portfolio_posts):
        try:
            process_portfolio_post(md_file)
            total_processed += 1
        except Exception as e:
            print(f"\n❌ Error processing {md_file.name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"✅ COMPLETE: Processed {total_processed}/{len(portfolio_posts)} posts")
    print("=" * 60)

    # Show folders created
    if PORTFOLIO_IMAGES.exists():
        folders = [d for d in PORTFOLIO_IMAGES.iterdir() if d.is_dir()]
        print(f"\n📁 Created {len(folders)} portfolio image folders")

        # Show folders with no images
        empty_folders = [d.name for d in folders if not any(d.iterdir())]
        if empty_folders:
            print(f"\n⚠️  {len(empty_folders)} folders have no images:")
            for folder in empty_folders[:10]:
                print(f"   - {folder}")
            if len(empty_folders) > 10:
                print(f"   ... and {len(empty_folders) - 10} more")

if __name__ == "__main__":
    main()
