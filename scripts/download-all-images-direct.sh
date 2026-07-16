#!/bin/bash
# Download ALL images directly from ikropka.eu using wget mirror
# This downloads the entire site including all images

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_DIR/scraped-content/images/original"

echo "Downloading ALL images from ikropka.eu..."
echo "This may take several minutes..."
echo "Output directory: $OUTPUT_DIR"
echo ""

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# Use wget to mirror the entire site and download all images
# --mirror: mirror site
# --convert-links: convert links for offline viewing (optional)
# --adjust-extension: add .html to files
# --page-requisites: download all page requisites (CSS, images, etc.)
# --no-parent: don't ascend to parent directory
# -A: accept only these file types
# --wait: wait between requests (be nice to server)
# --random-wait: randomize wait time
# --user-agent: identify ourselves

wget --mirror \
     --convert-links \
     --adjust-extension \
     --page-requisites \
     --no-parent \
     --accept jpg,jpeg,png,gif,webp,svg \
     --wait=0.5 \
     --random-wait \
     --user-agent="Mozilla/5.0 (compatible; IkropkaMigrationBot/1.0)" \
     --no-clobber \
     --domains=ikropka.eu \
     https://ikropka.eu/ 2>&1 | tee "$PROJECT_DIR/scraped-content/wget-download-log.txt"

echo ""
echo "Download complete!"
echo ""

# Count downloaded images
TOTAL=$(find ikropka.eu/wp-content/uploads -type f 2>/dev/null | wc -l)
echo "Downloaded $TOTAL image files"

# Move all images to flat directory structure (organized by year/month from WP uploads)
echo "Organizing images..."
find ikropka.eu/wp-content/uploads -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.webp" -o -iname "*.svg" \) -exec mv {} . \; 2>/dev/null || true

# Clean up directory structure
rm -rf ikropka.eu

FINAL_COUNT=$(find . -maxdepth 1 -type f | wc -l)
echo ""
echo "✓ Organized $FINAL_COUNT images in $OUTPUT_DIR"
echo ""
echo "Next steps:"
echo "  1. Run deduplication: node scripts/deduplicate-wp-thumbnails.js"
echo "  2. Run optimization: ./scripts/optimize-images.sh"
