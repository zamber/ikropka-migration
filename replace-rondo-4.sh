#!/bin/bash
cp "/home/luna/final-source-images/kwiaty-rondzie-pos17.jpg" \
   "docs/assets/images/portfolio/kwiaty-na-rondzie-ogrod-miejski/kwiaty-na-rondzie_ikropka_zdj70.jpg"
cp "/home/luna/final-source-images/kwiaty-rondzie-pos18.jpg" \
   "docs/assets/images/portfolio/kwiaty-na-rondzie-ogrod-miejski/kwiaty-na-rondzie_ikropka_zdj80.jpg"
cp "/home/luna/final-source-images/kwiaty-rondzie-pos19.jpg" \
   "docs/assets/images/portfolio/kwiaty-na-rondzie-ogrod-miejski/kwiaty-na-rondzie_ikropka_zdj90.jpg"
cp "/home/luna/final-source-images/kwiaty-rondzie-pos20.jpg" \
   "docs/assets/images/portfolio/kwiaty-na-rondzie-ogrod-miejski/kwiaty-na-rondzie_ikropka_zdj91.jpg"

# Verify
for f in docs/assets/images/portfolio/kwiaty-na-rondzie-ogrod-miejski/kwiaty-na-rondzie_ikropka_zdj{70,80,90,91}.jpg; do
  mime=$(file --mime-type -b "$f")
  size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f")
  echo "$(basename $f): $size bytes, $mime"
done
