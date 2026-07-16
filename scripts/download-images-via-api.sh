#!/bin/bash
# Download all images via WordPress REST API
# More reliable than wget scraping

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_DIR/scraped-content/images/original"
API_BASE="https://ikropka.eu/wp-json/wp/v2/media"

echo "Downloading images via WordPress REST API..."
echo "Output: $OUTPUT_DIR"
echo ""

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# Fetch all media paginated (100 per page)
PAGE=1
TOTAL_DOWNLOADED=0

while true; do
    echo "Fetching page $PAGE..."

    RESPONSE=$(curl -s "${API_BASE}?per_page=100&page=${PAGE}")

    # Check if response is empty array (no more pages)
    if [ "$RESPONSE" = "[]" ]; then
        echo "No more pages. Done!"
        break
    fi

    # Extract source_url from each media item
    echo "$RESPONSE" | grep -oE '"source_url":"[^"]+"' | \
        sed -E 's/"source_url":"([^"]+)"/\1/' | \
        while read -r url; do
            # Get filename from URL
            FILENAME=$(basename "$url")

            # Skip if already downloaded
            if [ -f "$FILENAME" ]; then
                echo "  Skip: $FILENAME (already exists)"
                continue
            fi

            # Download image
            echo "  Downloading: $FILENAME"
            wget -q --no-clobber "$url" -O "$FILENAME" 2>/dev/null || {
                echo "  WARNING: Failed to download $FILENAME"
            }

            TOTAL_DOWNLOADED=$((TOTAL_DOWNLOADED + 1))
        done

    PAGE=$((PAGE + 1))

    # Be polite - wait between page requests
    sleep 1
done

# Count final total
FINAL_COUNT=$(find . -type f | wc -l)

echo ""
echo "=============================="
echo "Download Complete"
echo "=============================="
echo "Total images: $FINAL_COUNT"
echo "Output directory: $OUTPUT_DIR"
echo ""
echo "Next steps:"
echo "  1. Deduplicate: node scripts/deduplicate-wp-thumbnails.js"
echo "  2. Optimize: ./scripts/optimize-images.sh"
