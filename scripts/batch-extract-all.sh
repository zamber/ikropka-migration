#!/bin/bash
# Batch extraction script for all ikropka.eu pages

API_KEY="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"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
EXTRACT_SCRIPT="$SCRIPT_DIR/extract-content.py"
URL_FILE="/tmp/ikropka-urls-sorted.txt"
OUTPUT_DIR="$PROJECT_DIR/content-structured"

# Counters
TOTAL=0
SUCCESS=0
FAILED=0
SKIPPED=0

# Function to determine page type from URL
get_page_type() {
    local url="$1"

    if [[ "$url" == "https://ikropka.eu/" ]]; then
        echo "homepage"
    elif [[ "$url" == *"/o-nas/"* ]] || [[ "$url" == *"/kontakt/"* ]] || [[ "$url" == *"/referencje/"* ]]; then
        echo "about"
    elif [[ "$url" == *"/oferta/"* ]]; then
        echo "service"
    elif [[ "$url" == *"/projekt/"* ]]; then
        echo "portfolio"
    else
        # Assume blog post for all others
        echo "post"
    fi
}

# Function to generate output filename from URL
get_output_filename() {
    local url="$1"
    local page_type="$2"

    # Extract slug from URL
    local slug=$(echo "$url" | sed 's|https://ikropka.eu/||' | sed 's|/$||' | tr '/' '-')

    if [ -z "$slug" ]; then
        slug="homepage"
    fi

    # Create subdirectory based on type
    local subdir=""
    case "$page_type" in
        homepage|about)
            subdir="pages"
            ;;
        service)
            subdir="services"
            ;;
        portfolio)
            subdir="portfolio"
            ;;
        post)
            subdir="posts"
            ;;
    esac

    echo "$OUTPUT_DIR/$subdir/${slug}.yaml"
}

echo "==================================="
echo "IKROPKA Batch Content Extraction"
echo "==================================="
echo ""
echo "URL file: $URL_FILE"
echo "Output dir: $OUTPUT_DIR"
echo ""

# Create output directories
mkdir -p "$OUTPUT_DIR"/{pages,services,portfolio,posts}

# Count total URLs
TOTAL=$(wc -l < "$URL_FILE")
echo "Total URLs to process: $TOTAL"
echo ""

# Process each URL
CURRENT=0
while IFS= read -r url; do
    CURRENT=$((CURRENT + 1))

    # Determine page type
    page_type=$(get_page_type "$url")

    # Generate output filename
    output_file=$(get_output_filename "$url" "$page_type")

    # Check if already extracted
    if [ -f "$output_file" ]; then
        echo "[$CURRENT/$TOTAL] SKIP: $url (already exists)"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    echo "[$CURRENT/$TOTAL] Extracting: $url"
    echo "  Type: $page_type"
    echo "  Output: $(basename $output_file)"

    # Run extraction
    python3 "$EXTRACT_SCRIPT" \
        --url "$url" \
        --type "$page_type" \
        --output "$output_file" \
        --api-key "$API_KEY" \
        > /tmp/extract-output-$CURRENT.log 2>&1

    if [ $? -eq 0 ]; then
        echo "  ✅ Success"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "  ❌ Failed (see /tmp/extract-output-$CURRENT.log)"
        FAILED=$((FAILED + 1))
    fi

    # Small delay to avoid rate limiting
    sleep 2

done < "$URL_FILE"

echo ""
echo "==================================="
echo "Extraction Complete"
echo "==================================="
echo "Total:   $TOTAL"
echo "Success: $SUCCESS"
echo "Failed:  $FAILED"
echo "Skipped: $SKIPPED"
echo ""
echo "Output directory: $OUTPUT_DIR"
echo ""

if [ $FAILED -gt 0 ]; then
    echo "⚠️  Some extractions failed. Check logs in /tmp/extract-output-*.log"
    exit 1
else
    echo "✅ All extractions successful!"
    exit 0
fi
