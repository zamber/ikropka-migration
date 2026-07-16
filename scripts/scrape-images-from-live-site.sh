#!/bin/bash
# Scrape image URLs directly from live ikropka.eu site
# Uses wget to mirror site structure and extract image references

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_FILE="$PROJECT_DIR/scraped-content/images/image-urls.txt"
TEMP_DIR="$PROJECT_DIR/scraped-content/temp-html"

echo "Scraping ikropka.eu for image URLs..."
mkdir -p "$TEMP_DIR"
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Use wget to download HTML pages (not images yet, just HTML)
echo "Downloading HTML pages to extract image references..."
cd "$TEMP_DIR"

wget --recursive \
     --level=3 \
     --no-parent \
     --no-clobber \
     --html-extension \
     --reject jpg,jpeg,png,gif,webp,svg,pdf,zip,tar,gz \
     --domains=ikropka.eu \
     --wait=1 \
     --random-wait \
     --user-agent="Mozilla/5.0 (compatible; IkropkaMigrationBot/1.0)" \
     https://ikropka.eu/ 2>&1 | tee "$PROJECT_DIR/scraped-content/wget-log.txt"

echo ""
echo "Extracting image URLs from downloaded HTML..."

# Find all HTML files and extract image URLs
find . -name "*.html" -type f -exec grep -hoE '(src|href)="[^"]*\.(jpg|jpeg|png|gif|webp|svg)"' {} \; | \
    sed -E 's/(src|href)="([^"]+)"/\2/' | \
    sort -u > temp-urls.txt

# Convert relative URLs to absolute
while IFS= read -r url; do
    if [[ "$url" == http* ]]; then
        echo "$url"
    elif [[ "$url" == /* ]]; then
        echo "https://ikropka.eu$url"
    elif [[ "$url" == ../* ]]; then
        # Skip complex relative paths for now
        continue
    else
        echo "https://ikropka.eu/$url"
    fi
done < temp-urls.txt | grep ikropka | sort -u > "$OUTPUT_FILE"

# Clean up temp files
rm -f temp-urls.txt

COUNT=$(wc -l < "$OUTPUT_FILE")
echo ""
echo "✓ Found $COUNT unique image URLs"
echo "✓ Saved to: $OUTPUT_FILE"

if [ "$COUNT" -gt 0 ]; then
    echo ""
    echo "Sample URLs (first 15):"
    head -15 "$OUTPUT_FILE"
fi

echo ""
echo "HTML files saved in: $TEMP_DIR"
echo "You can delete this directory after image download completes."
