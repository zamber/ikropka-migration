#!/bin/bash
set -e

BASE_URL="https://ikropka.eu"
PROJECT_DIR="/home/luna/ikropka-migration"
IMAGES_FILE="$PROJECT_DIR/scripts/missing-images.txt"
DOCS_DIR="$PROJECT_DIR/docs"

echo "Fetching missing images from ikropka.eu..."
echo "-------------------------------------------"

while IFS= read -r image_path; do
    # Skip empty lines
    [ -z "$image_path" ] && continue

    # Remove leading slash
    clean_path="${image_path#/}"

    # Full local path
    local_file="$DOCS_DIR/$clean_path"
    local_dir=$(dirname "$local_file")

    # URL to fetch from
    source_url="$BASE_URL/$clean_path"

    echo ""
    echo "Processing: $image_path"

    # Create directory if needed
    mkdir -p "$local_dir"

    # Try to fetch with curl
    if curl -f -s -L "$source_url" -o "$local_file"; then
        echo "  ✓ Downloaded: $source_url"

        # Get file size
        size=$(du -h "$local_file" | cut -f1)
        echo "  ✓ Size: $size"
    else
        echo "  ✗ Failed to download: $source_url"
        # Try alternative URL with different encoding
        alt_url=$(echo "$source_url" | sed 's/%C4%99/ę/g; s/%C5%82/ł/g; s/%C3%B3/ó/g')
        if [ "$alt_url" != "$source_url" ]; then
            echo "  → Trying alternative URL..."
            if curl -f -s -L "$alt_url" -o "$local_file"; then
                echo "  ✓ Downloaded: $alt_url"
                size=$(du -h "$local_file" | cut -f1)
                echo "  ✓ Size: $size"
            else
                echo "  ✗ Also failed: $alt_url"
            fi
        fi
    fi
done < "$IMAGES_FILE"

echo ""
echo "-------------------------------------------"
echo "Download complete!"
echo ""
echo "Downloaded images:"
find "$DOCS_DIR/assets/images/portfolio" -type f -mmin -5 -name "*.jpg" -o -name "*.png" | wc -l
