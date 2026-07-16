#!/bin/bash
# Extract all image URLs from ikropka.eu site analysis
# Output: scraped-content/images/image-urls.txt

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ANALYSIS_FILE="$PROJECT_DIR/analysis/site-scrape.md"
OUTPUT_FILE="$PROJECT_DIR/scraped-content/images/image-urls.txt"

echo "Extracting image URLs from $ANALYSIS_FILE..."

# Create output directory
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Extract URLs from analysis file - simpler approach
grep -oE 'https?://ikropka\.eu/[^[:space:]"\)]+\.(jpg|jpeg|png|gif|webp|svg)' "$ANALYSIS_FILE" | sort -u > "$OUTPUT_FILE" || true

# Remove duplicates and sort
sort -u "$OUTPUT_FILE" -o "$OUTPUT_FILE"

COUNT=$(wc -l < "$OUTPUT_FILE")
echo "Found $COUNT unique image URLs"
echo "Saved to: $OUTPUT_FILE"

# Show first 10 URLs
if [ "$COUNT" -gt 0 ]; then
    echo ""
    echo "First 10 URLs:"
    head -10 "$OUTPUT_FILE"
else
    echo "WARNING: No image URLs found in analysis file!"
    echo "Trying alternative method: scraping live site with wget spider..."

    # Fallback: Use wget to spider the site and extract image URLs
    wget --spider --force-html -r -l2 -nd -nv -H -Dik ropka.eu \
         -A jpg,jpeg,png,gif,webp,svg \
         https://ikropka.eu 2>&1 | \
         grep -oE 'https?://[^[:space:]]+\.(jpg|jpeg|png|gif|webp|svg)' | \
         grep ikropka | sort -u > "$OUTPUT_FILE"

    COUNT=$(wc -l < "$OUTPUT_FILE")
    echo "Found $COUNT image URLs via live scraping"
fi
