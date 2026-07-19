#!/bin/bash
#
# Check translation progress
#

cd "$(dirname "$0")/.."

echo "======================================"
echo "  Translation Progress Monitor"
echo "======================================"
echo ""
echo "Timestamp: $(date)"
echo ""

# Count files
en_portfolio=$(ls docs/en/_portfolio/*.md 2>/dev/null | wc -l)
en_services=$(ls docs/en/_services/*.md 2>/dev/null | wc -l)
en_posts=$(ls docs/en/_posts/*.md 2>/dev/null | wc -l)
en_pages=$(ls docs/en/_pages/*.md 2>/dev/null | wc -l)
en_total=$((en_portfolio + en_services + en_posts + en_pages))

de_portfolio=$(ls docs/de/_portfolio/*.md 2>/dev/null | wc -l)
de_services=$(ls docs/de/_services/*.md 2>/dev/null | wc -l)
de_posts=$(ls docs/de/_posts/*.md 2>/dev/null | wc -l)
de_pages=$(ls docs/de/_pages/*.md 2>/dev/null | wc -l)
de_total=$((de_portfolio + de_services + de_posts + de_pages))

total_files=147
total_translations=294

echo "ENGLISH (EN):"
echo "  Portfolio: $en_portfolio/72"
echo "  Services:  $en_services/9"
echo "  Posts:     $en_posts/60"
echo "  Pages:     $en_pages/6"
echo "  TOTAL:     $en_total/$total_files ($(echo "scale=1; $en_total*100/$total_files" | bc)%)"
echo ""

echo "GERMAN (DE):"
echo "  Portfolio: $de_portfolio/72"
echo "  Services:  $de_services/9"
echo "  Posts:     $de_posts/60"
echo "  Pages:     $de_pages/6"
echo "  TOTAL:     $de_total/$total_files ($(echo "scale=1; $de_total*100/$total_files" | bc)%)"
echo ""

overall_done=$((en_total + de_total))
echo "OVERALL PROGRESS: $overall_done/$total_translations translations ($(echo "scale=1; $overall_done*100/$total_translations" | bc)%)"
echo ""

# Check if process is running
if ps aux | grep -v grep | grep -q "batch-translate-all.sh"; then
    echo "Status: ✅ Batch translation process RUNNING"
    echo ""
    echo "Last 5 log entries:"
    tail -5 /tmp/batch-translation-final.log 2>/dev/null || echo "(No log available)"
else
    echo "Status: ⚠️  Batch translation process NOT RUNNING"
    echo ""
    if [ $overall_done -eq $total_translations ]; then
        echo "✅ Translation appears COMPLETE!"
    else
        echo "⚠️  Translation incomplete - may need to restart"
    fi
fi

echo ""
echo "======================================"
