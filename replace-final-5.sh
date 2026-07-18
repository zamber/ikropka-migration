#!/bin/bash
cp "/home/luna/final-source-images/park-kieszonkowy-ogrod-pereca-pos17.jpg" \
   "docs/assets/images/portfolio/park-kieszonkowy-ogrod-pereca/Ogrody-Pereca-zdj-8.jpg"
cp "/home/luna/final-source-images/park-kieszonkowy-ogrod-pereca-pos18.jpg" \
   "docs/assets/images/portfolio/park-kieszonkowy-ogrod-pereca/Ogrody-Pereca-zdj-5.jpg"
cp "/home/luna/final-source-images/park-kieszonkowy-ogrod-pereca-pos19.jpg" \
   "docs/assets/images/portfolio/park-kieszonkowy-ogrod-pereca/Ogrody-Pereca-zdj-9-min.jpg"
cp "/home/luna/final-source-images/park-kieszonkowy-ogrod-pereca-pos20.jpg" \
   "docs/assets/images/portfolio/park-kieszonkowy-ogrod-pereca/Ogrody-Pereca-zdj-10.jpg"
cp "/home/luna/final-source-images/park-kieszonkowy-ogrod-pereca-pos21.jpg" \
   "docs/assets/images/portfolio/park-kieszonkowy-ogrod-pereca/park-kieszonkowy-pereca-realizacja3-min_optimized.jpg"

# Verify
for f in docs/assets/images/portfolio/park-kieszonkowy-ogrod-pereca/{Ogrody-Pereca-zdj-{8,5,9-min,10},park-kieszonkowy-pereca-realizacja3-min_optimized}.jpg; do
  mime=$(file --mime-type -b "$f")
  size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f")
  echo "$(basename $f): $size bytes, $mime"
done
