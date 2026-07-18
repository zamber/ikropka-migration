#!/usr/bin/env node
/**
 * Extract blog post dates from ikropka.eu/aktualnosci/
 * Match by title to get original publication dates
 */

import { execSync } from 'child_process';
import { readFileSync, writeFileSync, readdirSync } from 'fs';

const POSTS_DIR = 'docs/_posts';
const files = readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));

console.log(`=== Extracting dates for ${files.length} blog posts ===\n`);

const results = {};
let found = 0;
let notFound = 0;

for (const file of files) {
  const filePath = `${POSTS_DIR}/${file}`;
  const content = readFileSync(filePath, 'utf-8');

  // Extract title from frontmatter
  const titleMatch = content.match(/^title:\s*["|']?([^"\n]+)["|']?$/m);
  if (!titleMatch) {
    console.log(`⚠ ${file.padEnd(60)} no title in frontmatter`);
    notFound++;
    continue;
  }

  const title = titleMatch[1].trim();
  const slug = file.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace('.md', '');

  process.stdout.write(`${title.substring(0, 50).padEnd(52)} `);

  // Try URL by slug
  const url = `https://ikropka.eu/${slug}/`;

  try {
    // Fetch HTML
    const html = execSync(`curl -sL "${url}"`, { encoding: 'utf-8', timeout: 10000 });

    // Check if redirected
    if (html.includes('<title>IKROPKA</title>') && !html.includes(title.substring(0, 20))) {
      console.log('❌ 404/redirect');
      results[file] = { url, found: false, reason: '404', title };
      notFound++;
      continue;
    }

    // Extract date - Strategy 1: <time> tag
    let dateMatch = html.match(/<time[^>]*datetime="([^"]+)"/);
    if (dateMatch) {
      const datetime = dateMatch[1];
      const date = datetime.split('T')[0]; // YYYY-MM-DD
      console.log(`✓ ${date} (time tag)`);
      results[file] = { url, found: true, date, source: 'time tag', title };
      found++;
      continue;
    }

    // Strategy 2: article:published_time meta
    dateMatch = html.match(/<meta\s+property="article:published_time"\s+content="([^"]+)"/);
    if (dateMatch) {
      const datetime = dateMatch[1];
      const date = datetime.split('T')[0];
      console.log(`✓ ${date} (meta)`);
      results[file] = { url, found: true, date, source: 'meta tag', title };
      found++;
      continue;
    }

    // Strategy 3: Date in text (Polish format)
    dateMatch = html.match(/(\d{1,2})\s+(stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia)\s+(\d{4})/i);
    if (dateMatch) {
      const months = {
        'stycznia': '01', 'lutego': '02', 'marca': '03', 'kwietnia': '04',
        'maja': '05', 'czerwca': '06', 'lipca': '07', 'sierpnia': '08',
        'września': '09', 'października': '10', 'listopada': '11', 'grudnia': '12'
      };
      const day = dateMatch[1].padStart(2, '0');
      const month = months[dateMatch[2].toLowerCase()];
      const year = dateMatch[3];
      const date = `${year}-${month}-${day}`;
      console.log(`✓ ${date} (text)`);
      results[file] = { url, found: true, date, source: 'text', title };
      found++;
      continue;
    }

    console.log('⚠ No date');
    results[file] = { url, found: false, reason: 'no date', title };
    notFound++;

  } catch (error) {
    console.log(`✗ Error: ${error.message.substring(0, 30)}`);
    results[file] = { url, found: false, reason: error.message, title };
    notFound++;
  }
}

writeFileSync('blog-dates.json', JSON.stringify(results, null, 2));

console.log(`\n${'='.repeat(60)}`);
console.log(`Found: ${found}, Not found: ${notFound}`);
console.log(`Results: blog-dates.json`);
