#!/usr/bin/env node
/**
 * Phase 3.2: Replace Broken Images
 *
 * Replace HTML files with real images from matched sources
 * Output: Replacement log and statistics
 */

import { readFileSync, writeFileSync, copyFileSync, statSync } from 'fs';
import { execSync } from 'child_process';

const FIX_STRATEGY = 'fix-strategy.json';
const LOG_FILE = 'replacement-log.txt';

console.log('=== Phase 3.2: Replacing Broken Images ===\n');

// Load fix strategy
const fixStrategy = JSON.parse(readFileSync(FIX_STRATEGY, 'utf-8'));
const matchedImages = Object.entries(fixStrategy).filter(([, data]) => data.confidence > 0);

console.log(`Found ${matchedImages.length} images to replace\n`);

const log = [];
let replaced = 0;
let skipped = 0;
let errors = 0;

for (const [imagePath, data] of matchedImages) {
  const destPath = imagePath.startsWith('/') ? imagePath.substring(1) : imagePath;
  const fullDestPath = `docs/${destPath}`;
  const sourcePath = data.sourceUrl;

  try {
    // Verify source exists and is an image
    const sourceStat = statSync(sourcePath);
    const sourceMime = execSync(`file --mime-type -b "${sourcePath}"`, { encoding: 'utf-8' }).trim();

    if (!sourceMime.startsWith('image/')) {
      console.log(`⚠ Skip ${data.filename}: source is not an image (${sourceMime})`);
      log.push(`SKIP,${imagePath},source not image,${sourceMime}`);
      skipped++;
      continue;
    }

    // Verify source is larger than HTML placeholder
    if (sourceStat.size <= 51414) {
      console.log(`⚠ Skip ${data.filename}: source too small (${sourceStat.size} bytes)`);
      log.push(`SKIP,${imagePath},source too small,${sourceStat.size}`);
      skipped++;
      continue;
    }

    // Get current file info
    const destStat = statSync(fullDestPath);
    const destMime = execSync(`file --mime-type -b "${fullDestPath}"`, { encoding: 'utf-8' }).trim();

    // Sanity check: dest should be HTML
    if (destMime !== 'text/html') {
      console.log(`⚠ Skip ${data.filename}: dest is already an image (${destMime})`);
      log.push(`SKIP,${imagePath},already image,${destMime}`);
      skipped++;
      continue;
    }

    // Replace file
    copyFileSync(sourcePath, fullDestPath);

    // Verify replacement
    const newStat = statSync(fullDestPath);
    const newMime = execSync(`file --mime-type -b "${fullDestPath}"`, { encoding: 'utf-8' }).trim();

    if (newMime.startsWith('image/')) {
      console.log(`✓ Replaced ${data.project}/${data.filename}`);
      console.log(`  ${destStat.size} bytes (${destMime}) → ${newStat.size} bytes (${newMime})`);
      log.push(`REPLACED,${imagePath},${destStat.size},${newStat.size},${data.strategy}`);
      replaced++;
    } else {
      console.log(`✗ Failed ${data.filename}: result is not an image (${newMime})`);
      log.push(`ERROR,${imagePath},result not image,${newMime}`);
      errors++;
    }

  } catch (error) {
    console.log(`✗ Error ${data.filename}: ${error.message}`);
    log.push(`ERROR,${imagePath},${error.message}`);
    errors++;
  }

  if ((replaced + skipped + errors) % 20 === 0) {
    console.log(`\nProgress: ${replaced + skipped + errors}/${matchedImages.length}`);
  }
}

// Write log
writeFileSync(LOG_FILE, log.join('\n'));

console.log('\n=== Replacement Complete ===');
console.log(`Total matched: ${matchedImages.length}`);
console.log(`✓ Replaced: ${replaced}`);
console.log(`⊘ Skipped: ${skipped}`);
console.log(`✗ Errors: ${errors}`);
console.log(`\nLog written to: ${LOG_FILE}`);

// Show breakdown by strategy
const strategyStats = {};
log.filter(l => l.startsWith('REPLACED')).forEach(line => {
  const strategy = line.split(',')[4];
  strategyStats[strategy] = (strategyStats[strategy] || 0) + 1;
});

console.log('\nReplaced by strategy:');
for (const [strategy, count] of Object.entries(strategyStats).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${strategy}: ${count}`);
}
