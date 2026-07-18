#!/usr/bin/env node
/**
 * Add date field to portfolio frontmatter based on scraped dates
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';

const PORTFOLIO_DIR = 'docs/_portfolio';
const DATES_FILE = 'project-dates-simple.json';

const dates = JSON.parse(readFileSync(DATES_FILE, 'utf-8'));
const files = readdirSync(PORTFOLIO_DIR).filter(f => f.endsWith('.md'));

console.log(`=== Adding dates to ${files.length} portfolio files ===\n`);

let updated = 0;
let skipped = 0;
let alreadyHas = 0;

for (const file of files) {
  const slug = file.replace('.md', '');
  const filePath = `${PORTFOLIO_DIR}/${file}`;
  const content = readFileSync(filePath, 'utf-8');

  // Check if already has date
  if (content.match(/^date:/m)) {
    console.log(`⊘ ${slug.padEnd(45)} already has date`);
    alreadyHas++;
    continue;
  }

  // Get date from scraped data
  const dateData = dates[slug];
  if (!dateData || !dateData.found) {
    console.log(`⚠ ${slug.padEnd(45)} no date available`);
    skipped++;
    continue;
  }

  const year = dateData.year;

  // Convert year to Jekyll date format
  // For ranges like "2015-2016", use the end year
  // For single year, use Dec 31 of that year (so newer projects sort first)
  let jekyllDate;
  if (year.includes('-')) {
    const endYear = year.split('-')[1];
    jekyllDate = `${endYear}-12-31`;
  } else {
    jekyllDate = `${year}-12-31`;
  }

  // Add date field after category in frontmatter
  const newContent = content.replace(
    /^(category: .+)$/m,
    `$1\ndate: ${jekyllDate}`
  );

  if (newContent === content) {
    console.log(`✗ ${slug.padEnd(45)} failed to add date (no category field?)`);
    skipped++;
    continue;
  }

  writeFileSync(filePath, newContent);
  console.log(`✓ ${slug.padEnd(45)} ${year} → ${jekyllDate}`);
  updated++;
}

console.log(`\n${'='.repeat(60)}`);
console.log(`Updated: ${updated}`);
console.log(`Already had date: ${alreadyHas}`);
console.log(`Skipped (no date): ${skipped}`);
