#!/usr/bin/env node
/**
 * Scrape project dates from ikropka.eu and add to portfolio frontmatter
 */

import { readFileSync, writeFileSync } from 'fs';
import { chromium } from 'playwright';

import { readdirSync } from 'fs';

const PORTFOLIO_DIR = 'docs/_portfolio';

console.log('=== Scraping Project Dates from ikropka.eu ===\n');

// Get all portfolio files
const files = readdirSync(PORTFOLIO_DIR).filter(f => f.endsWith('.md'));

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
const page = await context.newPage();

console.log(`Found ${files.length} portfolio files\n`);

const results = {};
let foundDates = 0;
let notFound = 0;

for (const file of files) {
  const slug = file.replace('.md', '');
  const filePath = `${PORTFOLIO_DIR}/${file}`;
  const content = readFileSync(filePath, 'utf-8');

  // Check if already has date
  if (content.match(/^date:/m)) {
    console.log(`  ⊘ ${slug}: already has date`);
    continue;
  }

  // Try original slug first
  let url = `https://ikropka.eu/projekt/${slug}/`;

  console.log(`📄 ${slug}`);
  console.log(`   Trying: ${url}`);

  try {
    const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });

    if (response.status() === 404 || response.url() === 'http://ikropka.eu/' || response.url() === 'https://ikropka.eu/') {
      console.log(`   ⚠ 404 or redirect to homepage`);
      notFound++;
      results[slug] = { url, found: false, reason: '404 or redirect' };
      continue;
    }

    // Extract date from page
    const dateInfo = await page.evaluate(() => {
      // Strategy 1: Look for "ROK | YYYY" or "ROK | YYYY-YYYY"
      const bodyText = document.body.innerText;
      const rokMatch = bodyText.match(/ROK\s*[|\:]\s*(\d{4}(?:-\d{4})?)/i);
      if (rokMatch) {
        return { year: rokMatch[1], source: 'ROK field' };
      }

      // Strategy 2: Look for "zrealizowana w YYYY"
      const realizMatch = bodyText.match(/zrealizow\w+\s+w\s+(\d{4})/i);
      if (realizMatch) {
        return { year: realizMatch[1], source: 'text: zrealizowana w' };
      }

      // Strategy 3: Post metadata
      const metaDate = document.querySelector('meta[property="article:published_time"]');
      if (metaDate) {
        return { year: metaDate.content.substring(0, 4), source: 'meta tag' };
      }

      return null;
    });

    if (dateInfo) {
      console.log(`   ✓ Found: ${dateInfo.year} (${dateInfo.source})`);
      results[slug] = { url, found: true, year: dateInfo.year, source: dateInfo.source };
      foundDates++;
    } else {
      console.log(`   ⚠ No date found on page`);
      results[slug] = { url, found: false, reason: 'no date on page' };
      notFound++;
    }

  } catch (error) {
    console.log(`   ✗ Error: ${error.message}`);
    results[slug] = { url, found: false, reason: error.message };
    notFound++;
  }

  // Small delay
  await new Promise(resolve => setTimeout(resolve, 500));
}

await browser.close();

// Write results
writeFileSync('project-dates.json', JSON.stringify(results, null, 2));

console.log('\n' + '='.repeat(60));
console.log('SCRAPING COMPLETE');
console.log('='.repeat(60));
console.log(`Total files: ${files.length}`);
console.log(`Dates found: ${foundDates}`);
console.log(`Not found: ${notFound}`);
console.log(`\nResults: project-dates.json`);
