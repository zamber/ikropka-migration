#!/usr/bin/env node
/**
 * Deduplicate WordPress thumbnail images
 * WordPress creates multiple sizes: image.jpg, image-300x200.jpg, image-1024x768.jpg
 * This script groups by base filename and keeps only the largest version
 */

const fs = require('fs');
const path = require('path');

const INPUT_DIR = path.join(__dirname, '../scraped-content/images/original');
const OUTPUT_DIR = path.join(__dirname, '../scraped-content/images/deduplicated');

console.log('WordPress Thumbnail Deduplication');
console.log('=================================\n');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Get all image files from input directory
if (!fs.existsSync(INPUT_DIR)) {
  console.error(`ERROR: Input directory not found: ${INPUT_DIR}`);
  console.error('Run image download script first!');
  process.exit(1);
}

const files = fs.readdirSync(INPUT_DIR).filter(f =>
  /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(f)
);

console.log(`Found ${files.length} image files in ${INPUT_DIR}\n`);

// Group files by base name
// Pattern: filename-123x456.jpg or filename-scaled.jpg
const groups = {};

files.forEach(file => {
  // Extract base name (remove size suffixes)
  let baseName = file
    .replace(/-\d+x\d+\.(jpg|jpeg|png|gif|webp|svg)$/i, '.$1')  // -300x200.jpg
    .replace(/-scaled\.(jpg|jpeg|png|gif|webp|svg)$/i, '.$1')   // -scaled.jpg
    .replace(/-e\d+\.(jpg|jpeg|png|gif|webp|svg)$/i, '.$1');    // -e1234567890.jpg

  if (!groups[baseName]) {
    groups[baseName] = [];
  }
  groups[baseName].push(file);
});

console.log(`Grouped into ${Object.keys(groups).length} unique base names\n`);

// For each group, find largest file and copy to output
let totalFiles = 0;
let keptFiles = 0;
let removedFiles = 0;

Object.entries(groups).forEach(([baseName, groupFiles]) => {
  totalFiles += groupFiles.length;

  if (groupFiles.length === 1) {
    // Only one file, just copy it
    const srcFile = path.join(INPUT_DIR, groupFiles[0]);
    const destFile = path.join(OUTPUT_DIR, groupFiles[0]);
    fs.copyFileSync(srcFile, destFile);
    keptFiles++;
    return;
  }

  // Multiple files - find largest
  let largestFile = null;
  let largestSize = 0;

  groupFiles.forEach(file => {
    const filePath = path.join(INPUT_DIR, file);
    const stats = fs.statSync(filePath);
    if (stats.size > largestSize) {
      largestSize = stats.size;
      largestFile = file;
    }
  });

  // Copy largest file
  const srcFile = path.join(INPUT_DIR, largestFile);
  const destFile = path.join(OUTPUT_DIR, largestFile);
  fs.copyFileSync(srcFile, destFile);

  keptFiles++;
  removedFiles += (groupFiles.length - 1);

  if (groupFiles.length > 2) {
    console.log(`Group "${baseName}":`);
    console.log(`  - Found ${groupFiles.length} versions`);
    console.log(`  - Kept: ${largestFile} (${(largestSize / 1024).toFixed(1)} KB)`);
    console.log(`  - Removed ${groupFiles.length - 1} duplicates\n`);
  }
});

console.log('\n=================================');
console.log('Deduplication Complete');
console.log('=================================');
console.log(`Total input files:    ${totalFiles}`);
console.log(`Kept (largest):       ${keptFiles}`);
console.log(`Removed (duplicates): ${removedFiles}`);
console.log(`Reduction:            ${((removedFiles / totalFiles) * 100).toFixed(1)}%`);
console.log(`\nOutput directory: ${OUTPUT_DIR}`);
