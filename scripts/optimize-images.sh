#!/bin/bash
# Optimize images: convert to WebP + create JPEG fallback
# Input: scraped-content/images/deduplicated/
# Output: site/assets/images/

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
INPUT_DIR="$PROJECT_DIR/scraped-content/images/deduplicated"
OUTPUT_DIR="$PROJECT_DIR/site/assets/images"

QUALITY=85
MAX_WIDTH=1600

echo "Image Optimization"
echo "=================="
echo "Input:  $INPUT_DIR"
echo "Output: $OUTPUT_DIR"
echo "Quality: $QUALITY%"
echo "Max width: ${MAX_WIDTH}px"
echo ""

# Check if input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo "ERROR: Input directory not found: $INPUT_DIR"
    echo "Run deduplication script first!"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Count files
TOTAL=$(find "$INPUT_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | wc -l)
echo "Found $TOTAL images to optimize"
echo ""

PROCESSED=0
ERRORS=0

# Process each image
find "$INPUT_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r img; do
    BASENAME=$(basename "$img")
    FILENAME="${BASENAME%.*}"
    EXTENSION="${BASENAME##*.}"

    PROCESSED=$((PROCESSED + 1))

    # Progress indicator
    if [ $((PROCESSED % 10)) -eq 0 ]; then
        echo "Progress: $PROCESSED/$TOTAL"
    fi

    # Resize and optimize JPEG/PNG (fallback)
    JPEG_OUT="$OUTPUT_DIR/${FILENAME}.jpg"
    convert "$img" \
        -resize "${MAX_WIDTH}x${MAX_WIDTH}>" \
        -quality $QUALITY \
        -strip \
        "$JPEG_OUT" 2>/dev/null || {
        echo "WARNING: Failed to convert $BASENAME to JPEG"
        ERRORS=$((ERRORS + 1))
        continue
    }

    # Convert to WebP
    WEBP_OUT="$OUTPUT_DIR/${FILENAME}.webp"
    cwebp -q $QUALITY "$JPEG_OUT" -o "$WEBP_OUT" >/dev/null 2>&1 || {
        echo "WARNING: Failed to convert $BASENAME to WebP"
        ERRORS=$((ERRORS + 1))
    }

done

echo ""
echo "=================="
echo "Optimization Complete"
echo "=================="
echo "Processed: $TOTAL images"
echo "Errors: $ERRORS"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Calculate size savings
ORIGINAL_SIZE=$(du -sb "$INPUT_DIR" | cut -f1)
OUTPUT_SIZE=$(du -sb "$OUTPUT_DIR" | cut -f1)
SAVED=$((ORIGINAL_SIZE - OUTPUT_SIZE))
SAVED_MB=$((SAVED / 1024 / 1024))
PERCENT=$((SAVED * 100 / ORIGINAL_SIZE))

echo "Size comparison:"
echo "  Original: $((ORIGINAL_SIZE / 1024 / 1024)) MB"
echo "  Optimized: $((OUTPUT_SIZE / 1024 / 1024)) MB"
echo "  Saved: ${SAVED_MB} MB (${PERCENT}%)"
