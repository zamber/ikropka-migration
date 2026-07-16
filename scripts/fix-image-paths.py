#!/usr/bin/env python3
"""Fix image paths in frontmatter to match flat directory structure."""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
IMAGES_DIR = DOCS_DIR / "assets/images"

# Build image filename -> actual path mapping
print("Building image index...")
image_map = {}
for img_file in IMAGES_DIR.rglob("*.jpg"):
    filename = img_file.name
    # Store relative path from docs/
    rel_path = "/" + str(img_file.relative_to(DOCS_DIR)).replace("\\", "/")
    image_map[filename] = rel_path
    
for img_file in IMAGES_DIR.rglob("*.png"):
    filename = img_file.name
    rel_path = "/" + str(img_file.relative_to(DOCS_DIR)).replace("\\", "/")
    image_map[filename] = rel_path

print(f"Found {len(image_map)} unique image filenames")

# Fix paths in portfolio
fixed_count = 0
for md_file in (DOCS_DIR / "_portfolio").glob("*.md"):
    content = md_file.read_text(encoding='utf-8')
    original = content
    
    # Fix featured_image paths
    def replace_path(match):
        full_path = match.group(1)
        filename = Path(full_path).name
        if filename in image_map:
            return f"featured_image: {image_map[filename]}"
        return match.group(0)
    
    content = re.sub(r'featured_image: (/assets/images/[^\s]+)', replace_path, content)
    
    # Fix gallery image paths
    def replace_gallery_path(match):
        full_path = match.group(1)
        filename = Path(full_path).name
        if filename in image_map:
            return f"  image: {image_map[filename]}"
        return match.group(0)
    
    content = re.sub(r'  image: (/assets/images/[^\s]+)', replace_gallery_path, content)
    
    if content != original:
        md_file.write_text(content, encoding='utf-8')
        fixed_count += 1
        print(f"✓ Fixed: {md_file.name}")

print(f"\n✅ Fixed {fixed_count} portfolio files")

# Fix paths in posts
fixed_posts = 0
for md_file in (DOCS_DIR / "_posts").glob("*.md"):
    content = md_file.read_text(encoding='utf-8')
    original = content
    
    # Fix header image paths
    def replace_header_path(match):
        full_path = match.group(1)
        filename = Path(full_path).name
        if filename in image_map:
            return f"  image: {image_map[filename]}"
        return match.group(0)
    
    content = re.sub(r'  image: (/assets/images/[^\s]+)', replace_header_path, content)
    
    # Fix markdown image paths
    def replace_md_image(match):
        alt = match.group(1)
        full_path = match.group(2)
        filename = Path(full_path).name
        if filename in image_map:
            return f"![{alt}]({image_map[filename]})"
        return match.group(0)
    
    content = re.sub(r'!\[([^\]]*)\]\((/assets/images/[^\)]+)\)', replace_md_image, content)
    
    if content != original:
        md_file.write_text(content, encoding='utf-8')
        fixed_posts += 1
        print(f"✓ Fixed: {md_file.name}")

print(f"\n✅ Fixed {fixed_posts} post files")
print(f"\n🎉 Total: {fixed_count + fixed_posts} files updated")
