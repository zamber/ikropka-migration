#!/usr/bin/env node
/**
 * Simple approach: scrape HTML from ikropka.eu/projekt/ pages
 * Extract dates using curl + regex (no Playwright needed)
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, readdirSync } from 'fs';

const PORTFOLIO_DIR = 'docs/_portfolio';
const files = readdirSync(PORTFOLIO_DIR).filter(f => f.endsWith('.md'));

console.log(`=== Extracting dates for ${files.length} projects ===\n`);

const results = {};
let found = 0;
let notFound = 0;

// Known slug mappings (from previous fixes)
const slugMappings = {
  'park-kieszonkowy-ogrod-pereca': 'park-kieszonkowy-ogrody-pereca',
  'kwiaty-na-rondzie-ogrod-miejski': 'kwiaty-rondzie-ogrod-miejski'
};

for (const file of files) { // All files
  const slug = file.replace('.md', '');
  const ikropkaSlug = slugMappings[slug] || slug;
  const url = `https://ikropka.eu/projekt/${ikropkaSlug}/`;

  process.stdout.write(`${slug.substring(0, 40).padEnd(42)} `);

  try {
    // Fetch HTML
    const html = execSync(`curl -sL "${url}"`, { encoding: 'utf-8', timeout: 10000 });

    // Check if redirected to homepage
    if (html.includes('<title>IKROPKA</title>') && !html.includes('projekt')) {
      console.log('❌ 404/redirect');
      results[slug] = { url, found: false, reason: '404' };
      notFound++;
      continue;
    }

    // Extract date - Strategy 1: ROK followed by <div class="text">YYYY</div>
    let dateMatch = html.match(/ROK<span>\|<\/span><\/div>\s*<div class="text">(\d{4}(?:-\d{4})?)<\/div>/);
    if (dateMatch) {
      const year = dateMatch[1];
      console.log(`✓ ${year} (ROK field)`);
      results[slug] = { url, found: true, year, source: 'ROK field' };
      found++;
      continue;
    }

    // Strategy 2: zrealizowana w YYYY
    dateMatch = html.match(/zrealizow\w+\s+w\s+(\d{4})/i);
    if (dateMatch) {
      const year = dateMatch[1];
      console.log(`✓ ${year} (text)`);
      results[slug] = { url, found: true, year, source: 'text: zrealizowana' };
      found++;
      continue;
    }

    // Strategy 3: article:published_time meta tag
    dateMatch = html.match(/<meta\s+property="article:published_time"\s+content="([^"]+)"/);
    if (dateMatch) {
      const year = dateMatch[1].substring(0, 4);
      console.log(`✓ ${year} (meta)`);
      results[slug] = { url, found: true, year, source: 'meta tag' };
      found++;
      continue;
    }

    console.log('⚠ No date');
    results[slug] = { url, found: false, reason: 'no date' };
    notFound++;

  } catch (error) {
    console.log(`✗ Error: ${error.message.substring(0, 30)}`);
    results[slug] = { url, found: false, reason: error.message };
    notFound++;
  }
}

writeFileSync('project-dates-simple.json', JSON.stringify(results, null, 2));

console.log(`\n${'='.repeat(60)}`);
console.log(`Found: ${found}, Not found: ${notFound}`);
console.log(`Results: project-dates-simple.json`);
