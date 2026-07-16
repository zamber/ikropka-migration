#!/bin/bash
set -e

PROJECT_DIR="/home/luna/ikropka-migration"
DOCS_DIR="$PROJECT_DIR/docs"
PORTFOLIO_DIR="$DOCS_DIR/assets/images/portfolio"

echo "Optimizing portfolio images..."
echo "==============================="
echo ""

# Counter
optimized=0
converted=0
skipped=0

# Find all JPG/PNG images in portfolio
find "$PORTFOLIO_DIR" -type f \( -name "*.jpg" -o -name "*.png" \) | head -10 | while read -r img; do
    filename=$(basename "$img")
    dirname=$(dirname "$img")

    # Get size
    size=$(stat -c%s "$img" 2>/dev/null || stat -f%z "$img" 2>/dev/null || echo 0)

    if [ $size -lt 10240 ]; then
        echo "⊘ Skipping $filename (already tiny: $(($size/1024))KB)"
        continue
    fi

    echo "Processing: $filename ($(($size/1024))KB)"

    # Create WebP version if doesn't exist
    webp_path="${img%.*}.webp"
    if [ ! -f "$webp_path" ]; then
        cwebp -q 85 "$img" -o "$webp_path" 2>/dev/null || true
        if [ -f "$webp_path" ]; then
            webp_size=$(stat -c%s "$webp_path" 2>/dev/null || stat -f%z "$webp_path" 2>/dev/null || echo 0)
            echo "  ✓ Created WebP: $(basename "$webp_path") ($(($webp_size/1024))KB)"
        fi
    else
        echo "  ⊘ WebP already exists"
    fi

    echo ""
done

echo "==============================="
echo "Optimization complete!"
