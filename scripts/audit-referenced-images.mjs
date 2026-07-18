#!/usr/bin/env node
/**
 * Phase 1.1: Audit Referenced Images
 *
 * Parse all portfolio markdown files and extract image references.
 * Output: referenced-images.json mapping image paths to posts that use them
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { basename } from 'path';

const PORTFOLIO_DIR = 'docs/_portfolio';
const OUTPUT_FILE = 'referenced-images.json';

console.log('=== Phase 1.1: Auditing Referenced Images ===\n');

const imageReferences = {}; // { imagePath: [postFiles] }
let totalImages = 0;
let totalPosts = 0;

// Read all portfolio markdown files
const portfolioFiles = readdirSync(PORTFOLIO_DIR).filter(f => f.endsWith('.md'));
console.log(`Found ${portfolioFiles.length} portfolio posts\n`);

for (const file of portfolioFiles) {
  const content = readFileSync(`${PORTFOLIO_DIR}/${file}`, 'utf-8');
  totalPosts++;

  // Extract frontmatter
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) {
    console.log(`⚠ No frontmatter in ${file}`);
    continue;
  }

  const frontmatter = frontmatterMatch[1];

  // Extract featured_image
  const featuredMatch = frontmatter.match(/featured_image:\s*(.+)/);
  if (featuredMatch) {
    const imagePath = featuredMatch[1].trim();
    if (!imageReferences[imagePath]) {
      imageReferences[imagePath] = [];
    }
    imageReferences[imagePath].push(file);
    totalImages++;
  }

  // Extract gallery images
  const galleryMatches = frontmatter.matchAll(/image_path:\s*(.+)/g);
  for (const match of galleryMatches) {
    const imagePath = match[1].trim();
    if (!imageReferences[imagePath]) {
      imageReferences[imagePath] = [];
    }
    if (!imageReferences[imagePath].includes(file)) {
      imageReferences[imagePath].push(file);
    }
    totalImages++;
  }

  const imageCount = (featuredMatch ? 1 : 0) + Array.from(frontmatter.matchAll(/image_path:/g)).length;
  console.log(`${file}: ${imageCount} images`);
}

// Write results
writeFileSync(OUTPUT_FILE, JSON.stringify(imageReferences, null, 2));

console.log('\n=== Audit Complete ===');
console.log(`Total posts: ${totalPosts}`);
console.log(`Total image references: ${totalImages}`);
console.log(`Unique images referenced: ${Object.keys(imageReferences).length}`);
console.log(`\nOutput written to: ${OUTPUT_FILE}`);

// Show sample
const samplePaths = Object.keys(imageReferences).slice(0, 5);
console.log('\nSample referenced images:');
samplePaths.forEach(path => {
  console.log(`  ${path} (used in ${imageReferences[path].length} post${imageReferences[path].length > 1 ? 's' : ''})`);
});
