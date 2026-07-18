#!/usr/bin/env node
/**
 * Phase 1.3: Match Broken Images to Sources
 *
 * Try multiple strategies to match broken images to available sources
 * Output: fix-strategy.json with confidence levels and source URLs
 */

import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { basename } from 'path';

const BROKEN_IMAGES = 'broken-referenced-images.json';
const IMAGE_URLS_JSON = '../COMPLETE-all-images-by-project.json';
const DOWNLOADED_DIR = '../downloaded-portfolio-images';
const MIRROR_DIR = 'scraped-content/images/original';
const OUTPUT_FILE = 'fix-strategy.json';

console.log('=== Phase 1.3: Matching Broken Images to Sources ===\n');

// Load data
const brokenImages = JSON.parse(readFileSync(BROKEN_IMAGES, 'utf-8'));
const imageUrlsByProject = JSON.parse(readFileSync(IMAGE_URLS_JSON, 'utf-8'));

// Index downloaded images
const downloadedFiles = existsSync(DOWNLOADED_DIR) ? readdirSync(DOWNLOADED_DIR) : [];
console.log(`Found ${downloadedFiles.length} already-downloaded images`);

// Index mirror images
const mirrorFiles = existsSync(MIRROR_DIR) ? readdirSync(MIRROR_DIR) : [];
console.log(`Found ${mirrorFiles.length} images in original mirror`);

console.log(`\nMatching ${Object.keys(brokenImages).length} broken images...\n`);

// Helper: Normalize filename (remove Polish chars, handle variants)
function normalize(str) {
  return decodeURIComponent(str)
    .replace(/ą/g, 'a').replace(/Ą/g, 'A')
    .replace(/ć/g, 'c').replace(/Ć/g, 'C')
    .replace(/ę/g, 'e').replace(/Ę/g, 'E')
    .replace(/ł/g, 'l').replace(/Ł/g, 'L')
    .replace(/ń/g, 'n').replace(/Ń/g, 'N')
    .replace(/ó/g, 'o').replace(/Ó/g, 'O')
    .replace(/ś/g, 's').replace(/Ś/g, 'S')
    .replace(/ź/g, 'z').replace(/Ź/g, 'Z')
    .replace(/ż/g, 'z').replace(/Ż/g, 'Z');
}

const fixStrategy = {};
let matchedCount = 0;
let unmatchedCount = 0;

for (const [imagePath, data] of Object.entries(brokenImages)) {
  const filename = basename(imagePath);
  const project = imagePath.split('/')[4]; // /assets/images/portfolio/PROJECT/file.jpg

  let isMatched = false;
  let strategy = null;
  let sourceUrl = null;
  let sourceType = null;
  let confidence = 0;

  // Strategy 1: Exact match in already-downloaded files
  if (downloadedFiles.includes(filename)) {
    strategy = 'downloaded-exact';
    sourceType = 'downloaded';
    sourceUrl = `${DOWNLOADED_DIR}/${filename}`;
    confidence = 100;
    isMatched = true;
  }

  // Strategy 1b: Filename match in downloaded (ends with target filename)
  if (!isMatched) {
    const matchingFile = downloadedFiles.find(f =>
      f.toLowerCase().endsWith(filename.toLowerCase()) ||
      f.toLowerCase().includes(filename.toLowerCase().replace(/\.(jpg|jpeg|png)$/i, ''))
    );
    if (matchingFile) {
      strategy = 'downloaded-suffix';
      sourceType = 'downloaded';
      sourceUrl = `${DOWNLOADED_DIR}/${matchingFile}`;
      confidence = 95;
      isMatched = true;
    }
  }

  // Strategy 2: Exact match in mirror
  if (!isMatched && mirrorFiles.includes(filename)) {
    strategy = 'mirror-exact';
    sourceType = 'mirror';
    sourceUrl = `${MIRROR_DIR}/${filename}`;
    confidence = 100;
    isMatched = true;
  }

  // Strategy 3: Find in project's URLs from ikropka.eu
  if (!isMatched && imageUrlsByProject[project]) {
    const projectUrls = imageUrlsByProject[project];

    // Try exact filename match
    for (const url of projectUrls) {
      const urlFilename = decodeURIComponent(basename(new URL(url).pathname));
      if (urlFilename === filename) {
        strategy = 'url-exact';
        sourceType = 'download';
        sourceUrl = url;
        confidence = 95;
        isMatched = true;
        break;
      }
    }

    // Try URL ends with filename (handles prefixed filenames)
    if (!isMatched) {
      for (const url of projectUrls) {
        const urlFilename = decodeURIComponent(basename(new URL(url).pathname)).toLowerCase();
        if (urlFilename.endsWith(filename.toLowerCase())) {
          strategy = 'url-suffix';
          sourceType = 'download';
          sourceUrl = url;
          confidence = 90;
          isMatched = true;
          break;
        }
      }
    }

    // Try normalized filename match
    if (!isMatched) {
      const normalizedTarget = normalize(filename);
      for (const url of projectUrls) {
        const urlFilename = normalize(decodeURIComponent(basename(new URL(url).pathname)));
        if (urlFilename === normalizedTarget) {
          strategy = 'url-normalized';
          sourceType = 'download';
          sourceUrl = url;
          confidence = 90;
          isMatched = true;
          break;
        }
      }
    }

    // Try fuzzy match (without -min, -scaled, etc.)
    if (!isMatched) {
      const baseTarget = filename.replace(/-min|-scaled|-optimized/g, '').replace(/\.(jpg|jpeg|png)$/i, '');
      for (const url of projectUrls) {
        const urlBase = basename(new URL(url).pathname).replace(/-min|-scaled|-optimized/g, '').replace(/\.(jpg|jpeg|png)$/i, '');
        if (normalize(urlBase) === normalize(baseTarget)) {
          strategy = 'url-fuzzy';
          sourceType = 'download';
          sourceUrl = url;
          confidence = 70;
          isMatched = true;
          break;
        }
      }
    }
  }

  // Strategy 4: Check downloaded with normalized name
  if (!isMatched) {
    const normalizedTarget = normalize(filename);
    const matchingDownloaded = downloadedFiles.find(f => normalize(f) === normalizedTarget);
    if (matchingDownloaded) {
      strategy = 'downloaded-normalized';
      sourceType = 'downloaded';
      sourceUrl = `${DOWNLOADED_DIR}/${matchingDownloaded}`;
      confidence = 85;
      isMatched = true;
    }
  }

  if (isMatched) {
    fixStrategy[imagePath] = {
      filename,
      project,
      strategy,
      sourceType,
      sourceUrl,
      confidence,
      posts: data.posts
    };
    matchedCount++;
  } else {
    fixStrategy[imagePath] = {
      filename,
      project,
      strategy: 'unmatched',
      sourceType: null,
      sourceUrl: null,
      confidence: 0,
      posts: data.posts
    };
    unmatchedCount++;
  }
}

// Write results
writeFileSync(OUTPUT_FILE, JSON.stringify(fixStrategy, null, 2));

console.log('\n=== Matching Complete ===');
console.log(`Total broken images: ${Object.keys(brokenImages).length}`);
console.log(`✓ Matched: ${matchedCount}`);
console.log(`✗ Unmatched: ${unmatchedCount}`);

// Breakdown by strategy
const strategyBreakdown = {};
for (const data of Object.values(fixStrategy)) {
  strategyBreakdown[data.strategy] = (strategyBreakdown[data.strategy] || 0) + 1;
}

console.log('\nMatching strategies:');
for (const [strategy, count] of Object.entries(strategyBreakdown).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${strategy}: ${count}`);
}

console.log(`\nOutput written to: ${OUTPUT_FILE}`);

// Show sample matches
const samples = Object.entries(fixStrategy).filter(([, d]) => d.confidence > 0).slice(0, 5);
console.log('\nSample matches:');
samples.forEach(([path, data]) => {
  console.log(`  ${basename(path)}`);
  console.log(`    ${data.strategy} (${data.confidence}% confidence)`);
  console.log(`    Source: ${data.sourceUrl}`);
});
