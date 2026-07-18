#!/usr/bin/env node
/**
 * Replace broken images with downloaded images from source pages
 */

import { readFileSync, copyFileSync, statSync } from 'fs';
import { execSync } from 'child_process';

const SOURCE_LOG = 'source-download-log.json';
const OUTPUT_LOG = 'final-replacement-log.txt';

console.log('=== Replacing Broken Images with Source Downloads ===\n');

const sourceLog = JSON.parse(readFileSync(SOURCE_LOG, 'utf-8'));
const log = [];
let replaced = 0;
let skipped = 0;
let errors = 0;

for (const [projectSlug, projectData] of Object.entries(sourceLog)) {
  if (!projectData.matches || projectData.matches.length === 0) {
    continue;
  }

  console.log(`\n📁 ${projectSlug} (${projectData.matches.length} images)`);

  for (const match of projectData.matches) {
    if (!match.downloadedPath) {
      console.log(`  ⚠ Skip ${match.repoFilename}: not downloaded`);
      skipped++;
      continue;
    }

    const sourcePath = match.downloadedPath;
    const destPath = match.repoPath.startsWith('/') ? match.repoPath.substring(1) : match.repoPath;
    const fullDestPath = `docs/${destPath}`;

    try {
      // Verify source exists and is an image
      const sourceStat = statSync(sourcePath);
      const sourceMime = execSync(`file --mime-type -b "${sourcePath}"`, { encoding: 'utf-8' }).trim();

      if (!sourceMime.startsWith('image/')) {
        console.log(`  ⚠ Skip ${match.repoFilename}: source not image (${sourceMime})`);
        log.push(`SKIP,${match.repoPath},source not image,${sourceMime}`);
        skipped++;
        continue;
      }

      // Get current file info
      const destStat = statSync(fullDestPath);
      const destMime = execSync(`file --mime-type -b "${fullDestPath}"`, { encoding: 'utf-8' }).trim();

      // Should be HTML
      if (destMime !== 'text/html') {
        console.log(`  ⚠ Skip ${match.repoFilename}: already an image (${destMime})`);
        log.push(`SKIP,${match.repoPath},already image,${destMime}`);
        skipped++;
        continue;
      }

      // Replace
      copyFileSync(sourcePath, fullDestPath);

      // Verify
      const newMime = execSync(`file --mime-type -b "${fullDestPath}"`, { encoding: 'utf-8' }).trim();
      const newStat = statSync(fullDestPath);

      if (newMime.startsWith('image/')) {
        console.log(`  ✓ ${match.repoFilename}: ${destStat.size} → ${newStat.size} bytes (${newMime})`);
        log.push(`REPLACED,${match.repoPath},${destStat.size},${newStat.size},position-${match.position}`);
        replaced++;
      } else {
        console.log(`  ✗ ${match.repoFilename}: result not image (${newMime})`);
        log.push(`ERROR,${match.repoPath},result not image,${newMime}`);
        errors++;
      }

    } catch (error) {
      console.log(`  ✗ ${match.repoFilename}: ${error.message}`);
      log.push(`ERROR,${match.repoPath},${error.message}`);
      errors++;
    }
  }
}

// Write log
import { writeFileSync } from 'fs';
writeFileSync(OUTPUT_LOG, log.join('\n'));

console.log('\n' + '='.repeat(60));
console.log('REPLACEMENT COMPLETE');
console.log('='.repeat(60));
console.log(`✓ Replaced: ${replaced}`);
console.log(`⊘ Skipped: ${skipped}`);
console.log(`✗ Errors: ${errors}`);
console.log(`\nLog: ${OUTPUT_LOG}`);

if (replaced > 0) {
  console.log('\n✅ Ready to commit and verify!');
}
