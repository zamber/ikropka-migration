#!/usr/bin/env python3
"""
Fix image paths in portfolio markdown frontmatter.

For each portfolio post:
1. Extract slug from filename
2. Update featured_image path to /assets/images/portfolio/{slug}/{filename}
3. Update all gallery image paths similarly
4. Write back to markdown file
"""

import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
PORTFOLIO_DIR = DOCS_DIR / "_portfolio"
PORTFOLIO_IMAGES = DOCS_DIR / "assets/images/portfolio"

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

def fix_image_path(image_path, slug):
    """
    Fix image path to use correct portfolio folder structure.
    /assets/images/portfolio/something/image.jpg -> /assets/images/portfolio/{slug}/image.jpg
    """
    if not image_path:
        return image_path

    filename = Path(image_path).name
    return f"/assets/images/portfolio/{slug}/{filename}"

def process_portfolio_post(md_file):
    """Process a single portfolio markdown file."""
    slug = md_file.stem
    print(f"📄 {slug}")

    # Parse frontmatter
    frontmatter, markdown_content = extract_frontmatter_and_content(md_file)

    if frontmatter is None:
        print(f"   ⚠️  Skipping (no valid frontmatter)")
        return

    # Track if anything changed
    changed = False

    # Fix featured_image
    if 'featured_image' in frontmatter and frontmatter['featured_image']:
        old_path = frontmatter['featured_image']
        new_path = fix_image_path(old_path, slug)

        if old_path != new_path:
            frontmatter['featured_image'] = new_path
            changed = True
            print(f"   ✓ Fixed featured_image")

    # Fix gallery images
    if 'gallery' in frontmatter and isinstance(frontmatter['gallery'], list):
        for i, gallery_item in enumerate(frontmatter['gallery']):
            if isinstance(gallery_item, dict) and 'image' in gallery_item:
                old_path = gallery_item['image']
                new_path = fix_image_path(old_path, slug)

                if old_path != new_path:
                    frontmatter['gallery'][i]['image'] = new_path
                    changed = True

    # Write back if changed
    if changed:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            f.write("---\n")
            f.write(markdown_content)
        print(f"   ✅ Updated")
    else:
        print(f"   ⏭️  No changes needed")

def main():
    """Main entry point."""
    print("=" * 60)
    print("🔧  FIX PORTFOLIO IMAGE PATHS")
    print("=" * 60)

    if not PORTFOLIO_DIR.exists():
        print(f"❌ Portfolio directory not found: {PORTFOLIO_DIR}")
        return

    # Get all portfolio posts
    portfolio_posts = sorted(PORTFOLIO_DIR.glob("*.md"))
    print(f"\n📚 Found {len(portfolio_posts)} portfolio posts\n")

    total_fixed = 0

    for md_file in portfolio_posts:
        try:
            process_portfolio_post(md_file)
            total_fixed += 1
        except Exception as e:
            print(f"\n❌ Error processing {md_file.name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"✅ COMPLETE: Fixed {total_fixed}/{len(portfolio_posts)} posts")
    print("=" * 60)

if __name__ == "__main__":
    main()
