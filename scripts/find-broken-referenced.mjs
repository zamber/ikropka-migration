#!/usr/bin/env node
/**
 * Phase 1.2: Find Broken Referenced Images
 *
 * Check each referenced image and identify which ones are HTML files
 * Output: broken-referenced-images.json
 */

import { readFileSync, writeFileSync, statSync, existsSync } from 'fs';
import { execSync } from 'child_process';

const REFERENCED_IMAGES = 'referenced-images.json';
const OUTPUT_FILE = 'broken-referenced-images.json';
const REPO_ROOT = 'docs'; // Portfolio images are in docs/assets/images/portfolio

console.log('=== Phase 1.2: Finding Broken Referenced Images ===\n');

// Load referenced images
const referencedImages = JSON.parse(readFileSync(REFERENCED_IMAGES, 'utf-8'));
const imagePaths = Object.keys(referencedImages);

console.log(`Checking ${imagePaths.length} referenced images...\n`);

const brokenImages = {};
let checkedCount = 0;
let brokenCount = 0;
let missingCount = 0;

for (const imagePath of imagePaths) {
  checkedCount++;

  // Convert /assets/... to docs/assets/...
  const filePath = imagePath.startsWith('/') ? imagePath.substring(1) : imagePath;
  const fullPath = `${REPO_ROOT}/${filePath}`;

  if (!existsSync(fullPath)) {
    console.log(`⚠ MISSING: ${imagePath}`);
    missingCount++;
    continue;
  }

  // Get file stats
  const stats = statSync(fullPath);

  // Check MIME type
  let mimeType;
  try {
    mimeType = execSync(`file --mime-type -b "${fullPath}"`, { encoding: 'utf-8' }).trim();
  } catch (error) {
    console.log(`✗ Error checking ${imagePath}: ${error.message}`);
    continue;
  }

  // If it's HTML, it's broken
  if (mimeType === 'text/html') {
    brokenCount++;
    brokenImages[imagePath] = {
      posts: referencedImages[imagePath],
      currentSize: stats.size,
      actualMime: mimeType,
      filePath: fullPath
    };

    if (brokenCount <= 10) {
      console.log(`✗ BROKEN: ${imagePath} (${stats.size} bytes, ${mimeType})`);
    }
  }

  if (checkedCount % 100 === 0) {
    console.log(`Progress: ${checkedCount}/${imagePaths.length} checked, ${brokenCount} broken so far...`);
  }
}

// Write results
writeFileSync(OUTPUT_FILE, JSON.stringify(brokenImages, null, 2));

console.log('\n=== Broken Image Analysis Complete ===');
console.log(`Total referenced images: ${imagePaths.length}`);
console.log(`Checked: ${checkedCount}`);
console.log(`✗ Broken (HTML): ${brokenCount}`);
console.log(`⚠ Missing: ${missingCount}`);
console.log(`✓ Working: ${checkedCount - brokenCount - missingCount}`);
console.log(`\nOutput written to: ${OUTPUT_FILE}`);

// Show breakdown by project
if (brokenCount > 0) {
  const projectBreakdown = {};
  for (const [imagePath, data] of Object.entries(brokenImages)) {
    const project = imagePath.split('/')[4]; // /assets/images/portfolio/PROJECT/...
    projectBreakdown[project] = (projectBreakdown[project] || 0) + 1;
  }

  const topProjects = Object.entries(projectBreakdown)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  console.log('\nTop 10 projects with broken images:');
  topProjects.forEach(([project, count]) => {
    console.log(`  ${project}: ${count} broken`);
  });
}
