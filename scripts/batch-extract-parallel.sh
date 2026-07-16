#!/bin/bash
# Parallel batch extraction for ikropka.eu pages

API_KEY="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"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
EXTRACT_SCRIPT="$SCRIPT_DIR/extract-content.py"
URL_FILE="/tmp/ikropka-urls-sorted.txt"
OUTPUT_DIR="$PROJECT_DIR/content-structured"
PARALLEL_JOBS=10  # Process 10 pages concurrently

# Function to determine page type from URL
get_page_type() {
    local url="$1"
    if [[ "$url" == "https://ikropka.eu/" ]]; then echo "homepage"
    elif [[ "$url" == *"/o-nas/"* ]] || [[ "$url" == *"/kontakt/"* ]] || [[ "$url" == *"/referencje/"* ]]; then echo "about"
    elif [[ "$url" == *"/oferta/"* ]]; then echo "service"
    elif [[ "$url" == *"/projekt/"* ]]; then echo "portfolio"
    else echo "post"
    fi
}

# Function to generate output filename
get_output_filename() {
    local url="$1"
    local page_type="$2"
    local slug=$(echo "$url" | sed 's|https://ikropka.eu/||' | sed 's|/$||' | tr '/' '-')
    [ -z "$slug" ] && slug="homepage"

    local subdir="pages"
    case "$page_type" in
        service) subdir="services" ;;
        portfolio) subdir="portfolio" ;;
        post) subdir="posts" ;;
    esac

    echo "$OUTPUT_DIR/$subdir/${slug}.yaml"
}

# Function to extract a single page
extract_page() {
    local url="$1"
    local page_type=$(get_page_type "$url")
    local output_file=$(get_output_filename "$url" "$page_type")

    # Skip if exists
    if [ -f "$output_file" ]; then
        echo "[SKIP] $url"
        return 0
    fi

    echo "[START] $url (type: $page_type)"

    python3 "$EXTRACT_SCRIPT" \
        --url "$url" \
        --type "$page_type" \
        --output "$output_file" \
        --api-key "$API_KEY" \
        > /tmp/extract-$(basename "$output_file" .yaml).log 2>&1

    if [ $? -eq 0 ]; then
        echo "[SUCCESS] $url"
        return 0
    else
        echo "[FAILED] $url"
        return 1
    fi
}

export -f extract_page
export -f get_page_type
export -f get_output_filename
export API_KEY EXTRACT_SCRIPT OUTPUT_DIR

echo "==================================="
echo "IKROPKA Parallel Batch Extraction"
echo "==================================="
echo "Parallel jobs: $PARALLEL_JOBS"
echo "Total URLs: $(wc -l < "$URL_FILE")"
echo ""

# Create output directories
mkdir -p "$OUTPUT_DIR"/{pages,services,portfolio,posts}

# Use xargs to process in parallel
cat "$URL_FILE" | xargs -P $PARALLEL_JOBS -I {} bash -c 'extract_page "$@"' _ {}

echo ""
echo "==================================="
echo "Extraction Complete!"
echo "==================================="
echo "Output files:"
find "$OUTPUT_DIR" -name "*.yaml" -type f | wc -l
echo ""
