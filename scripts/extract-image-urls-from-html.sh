#!/bin/bash
# Extract image URLs from downloaded HTML files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
HTML_DIR="$PROJECT_DIR/scraped-content/temp-html"
OUTPUT_FILE="$PROJECT_DIR/scraped-content/images/image-urls.txt"

echo "Extracting image URLs from HTML files..."
echo "HTML directory: $HTML_DIR"

# Find all image references in HTML files
grep -horE '(src|href|data-src)="[^"]*\.(jpg|jpeg|png|gif|webp|svg)"' "$HTML_DIR" 2>/dev/null | \
    sed -E 's/.*(src|href|data-src)="([^"]+)"/\2/' | \
    grep -E '\.(jpg|jpeg|png|gif|webp|svg)$' | \
    sort -u > /tmp/temp-urls.txt

# Also look for background images in CSS style attributes
grep -horE 'url\([^)]*\.(jpg|jpeg|png|gif|webp|svg)\)' "$HTML_DIR" 2>/dev/null | \
    sed -E 's/.*url\(["'\'']?([^"'\'']+)["'\'']?\)/\1/' | \
    grep -E '\.(jpg|jpeg|png|gif|webp|svg)$' >> /tmp/temp-urls.txt || true

# Convert relative URLs to absolute
while IFS= read -r url; do
    if [[ "$url" == https://ikropka.eu/* ]]; then
        echo "$url"
    elif [[ "$url" == http://ikropka.eu/* ]]; then
        echo "${url/http:/https:}"
    elif [[ "$url" == //ikropka.eu/* ]]; then
        echo "https:$url"
    elif [[ "$url" == /wp-content/* ]]; then
        echo "https://ikropka.eu$url"
    elif [[ "$url" == wp-content/* ]]; then
        echo "https://ikropka.eu/$url"
    fi
done < /tmp/temp-urls.txt | sort -u > "$OUTPUT_FILE"

# Clean up
rm -f /tmp/temp-urls.txt

COUNT=$(wc -l < "$OUTPUT_FILE")
echo ""
echo "✓ Found $COUNT unique image URLs"
echo "✓ Saved to: $OUTPUT_FILE"

if [ "$COUNT" -gt 0 ]; then
    echo ""
    echo "Sample URLs (first 20):"
    head -20 "$OUTPUT_FILE"
    echo ""
    echo "To download all images, run:"
    echo "  ./scripts/download-images.sh"
fi
