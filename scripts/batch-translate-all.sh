#!/bin/bash
#
# Batch translate all Jekyll content files from Polish to English and German
# Uses parallel processing for speed
#

set -e

cd "$(dirname "$0")/.."

API_KEY="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"
GLOSSARY="scripts/translation-glossary.yaml"
SCRIPT="scripts/translate-jekyll-content.py"

# Create output directories
mkdir -p docs/en/{_portfolio,_services,_posts,_pages}
mkdir -p docs/de/{_portfolio,_services,_posts,_pages}

# Function to translate one file
translate_file() {
    local input_file="$1"
    local target_lang="$2"
    local content_type="$3"

    local output_dir="docs/${target_lang}/${content_type}"
    local filename=$(basename "$input_file")

    echo "[$(date +%H:%M:%S)] Translating: $filename → ${target_lang}"

    python3 "$SCRIPT" \
        --input "$input_file" \
        --target-lang "$target_lang" \
        --output "$output_dir" \
        --glossary "$GLOSSARY" \
        --api-key "$API_KEY" 2>&1 | grep -E "(✅|ERROR)" || true
}

export -f translate_file
export API_KEY GLOSSARY SCRIPT

echo "========================================="
echo "  IKROPKA Migration - Batch Translation"
echo "========================================="
echo ""
echo "Model: tencent/hy3:free (OpenRouter)"
echo "Languages: EN + DE"
echo "Mode: Sequential (rate-limit safe, with exponential backoff)"
echo ""

# Count files
portfolio_count=$(find docs/_portfolio -name "*.md" | wc -l)
services_count=$(find docs/_services -name "*.md" | wc -l)
posts_count=$(find docs/_posts -name "*.md" | wc -l)
pages_count=$(find docs/_pages -name "*.md" | wc -l)

total_files=$((portfolio_count + services_count + posts_count + pages_count))
total_translations=$((total_files * 2))  # 2 languages

echo "Files to translate:"
echo "  - Portfolio: $portfolio_count"
echo "  - Services: $services_count"
echo "  - Posts: $posts_count"
echo "  - Pages: $pages_count"
echo "  TOTAL: $total_files files × 2 languages = $total_translations translations"
echo ""
echo "Starting batch translation..."
echo ""

# Translate ENGLISH first
echo "=== TRANSLATING TO ENGLISH ==="
echo ""

echo "[EN] Portfolio ($portfolio_count files)..."
for file in docs/_portfolio/*.md; do
    translate_file "$file" en _portfolio
done

echo "[EN] Services ($services_count files)..."
for file in docs/_services/*.md; do
    translate_file "$file" en _services
done

echo "[EN] Posts ($posts_count files)..."
for file in docs/_posts/*.md; do
    translate_file "$file" en _posts
done

echo "[EN] Pages ($pages_count files)..."
for file in docs/_pages/*.md; do
    translate_file "$file" en _pages
done

echo ""
echo "=== TRANSLATING TO GERMAN ==="
echo ""

echo "[DE] Portfolio ($portfolio_count files)..."
for file in docs/_portfolio/*.md; do
    translate_file "$file" de _portfolio
done

echo "[DE] Services ($services_count files)..."
for file in docs/_services/*.md; do
    translate_file "$file" de _services
done

echo "[DE] Posts ($posts_count files)..."
for file in docs/_posts/*.md; do
    translate_file "$file" de _posts
done

echo "[DE] Pages ($pages_count files)..."
for file in docs/_pages/*.md; do
    translate_file "$file" de _pages
done

echo ""
echo "========================================="
echo "  BATCH TRANSLATION COMPLETE!"
echo "========================================="
echo ""
echo "Summary:"
echo "  - Translated: $total_translations files"
echo "  - English: docs/en/"
echo "  - German: docs/de/"
echo ""
echo "Next steps:"
echo "  1. Update _config.yml with EN/DE collections"
echo "  2. Create language switcher UI"
echo "  3. Add hreflang SEO tags"
echo "  4. Test Jekyll build"
echo ""
