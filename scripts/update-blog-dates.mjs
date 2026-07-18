#!/usr/bin/env node
/**
 * Update blog post dates in filenames and frontmatter
 */

import { readFileSync, writeFileSync, renameSync, readdirSync } from 'fs';

const POSTS_DIR = 'docs/_posts';
const DATES_FILE = 'blog-dates.json';

const dates = JSON.parse(readFileSync(DATES_FILE, 'utf-8'));
const files = readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));

console.log(`=== Updating dates for ${files.length} blog posts ===\n`);

let updated = 0;
let skipped = 0;

for (const file of files) {
  const dateData = dates[file];

  if (!dateData || !dateData.found) {
    console.log(`⚠ ${file.padEnd(70)} no date available`);
    skipped++;
    continue;
  }

  const newDate = dateData.date;
  const oldFilePath = `${POSTS_DIR}/${file}`;
  const content = readFileSync(oldFilePath, 'utf-8');

  // Update date in frontmatter
  const newContent = content.replace(/^date:\s*.+$/m, `date: ${newDate}`);

  // Create new filename
  const slug = file.replace(/^\d{4}-\d{2}-\d{2}-/, '');
  const newFilename = `${newDate}-${slug}`;
  const newFilePath = `${POSTS_DIR}/${newFilename}`;

  // Check if file would be renamed
  if (file !== newFilename) {
    // Write updated content
    writeFileSync(oldFilePath, newContent);
    // Rename file
    renameSync(oldFilePath, newFilePath);
    console.log(`✓ ${file.padEnd(70)} → ${newDate}`);
  } else {
    // Just update content
    writeFileSync(oldFilePath, newContent);
    console.log(`✓ ${file.padEnd(70)} ${newDate} (no rename needed)`);
  }

  updated++;
}

console.log(`\n${'='.repeat(60)}`);
console.log(`Updated: ${updated}`);
console.log(`Skipped: ${skipped}`);
