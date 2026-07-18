#!/usr/bin/env node
/**
 * Download images directly from ikropka.eu project pages
 * Uses playwright to extract images, matches by position
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { execSync } from 'child_process';
import https from 'https';
import { createWriteStream } from 'fs';
import { chromium } from 'playwright';

const MAPPING_FILE = 'direct-image-mapping.json';
const DOWNLOAD_DIR = '../final-source-images';
const OUTPUT_LOG = 'source-download-log.json';

if (!existsSync(DOWNLOAD_DIR)) {
  mkdirSync(DOWNLOAD_DIR, { recursive: true });
}

function downloadFile(url, path) {
  return new Promise((resolve, reject) => {
    const file = createWriteStream(path);
    https.get(url, (response) => {
      if (response.statusCode === 301 || response.statusCode === 302) {
        file.close();
        downloadFile(response.headers.location, path).then(resolve).catch(reject);
        return;
      }
      if (response.statusCode !== 200) {
        file.close();
        reject(new Error(`HTTP ${response.statusCode}`));
        return;
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
      file.on('error', reject);
    }).on('error', reject);
  });
}

async function main() {
  console.log('=== Downloading Images from Source Pages ===\n');

  const projectMappings = JSON.parse(readFileSync(MAPPING_FILE, 'utf-8'));
  const projects = Object.entries(projectMappings).sort((a, b) => b[1].brokenCount - a[1].brokenCount);

  console.log(`Processing ${projects.length} projects...\n`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const results = {};
  let totalDownloaded = 0;
  let totalMatched = 0;
  let totalErrors = 0;

  for (const [projectSlug, projectData] of projects) {
    console.log(`\n📁 ${projectSlug} (${projectData.brokenCount} broken)`);
    console.log(`   Visiting: ${projectData.ikropkaUrl}`);

    try {
      await page.goto(projectData.ikropkaUrl, { waitUntil: 'networkidle', timeout: 30000 });

      // Extract ALL image URLs from the page IN ORDER
      const imageUrls = await page.evaluate(() => {
        const urls = [];

        // Strategy 1: Find gallery/slider images
        const galleryImages = document.querySelectorAll('img[src*="wp-content/uploads"]');
        galleryImages.forEach(img => {
          if (img.src && img.src.includes('wp-content/uploads')) {
            urls.push(img.src);
          }
        });

        // Strategy 2: Find images in lightbox links
        const lightboxLinks = document.querySelectorAll('a[href*="wp-content/uploads"]');
        lightboxLinks.forEach(a => {
          if (a.href && a.href.match(/\.(jpg|jpeg|png|gif)$/i)) {
            if (!urls.includes(a.href)) {
              urls.push(a.href);
            }
          }
        });

        // Remove duplicates while preserving order
        return [...new Set(urls)];
      });

      console.log(`   Found ${imageUrls.length} images on page`);

      // Match images by position
      const matches = [];
      for (const brokenImage of projectData.brokenImages) {
        const position = brokenImage.position;

        if (position < imageUrls.length) {
          const sourceUrl = imageUrls[position];
          matches.push({
            repoPath: brokenImage.path,
            repoFilename: brokenImage.filename,
            position,
            sourceUrl,
            type: brokenImage.type
          });
          totalMatched++;
        } else {
          console.log(`   ⚠ No image at position ${position} for ${brokenImage.filename}`);
        }
      }

      // Download matched images
      for (const match of matches) {
        try {
          const downloadPath = `${DOWNLOAD_DIR}/${projectSlug}-pos${match.position}.jpg`;

          console.log(`   ⬇ [${match.position}] ${match.repoFilename}`);
          console.log(`      ${match.sourceUrl}`);

          await downloadFile(match.sourceUrl, downloadPath);

          // Verify it's an image
          const mimeType = execSync(`file --mime-type -b "${downloadPath}"`, { encoding: 'utf-8' }).trim();
          if (mimeType.startsWith('image/')) {
            console.log(`      ✓ Downloaded (${mimeType})`);
            match.downloadedPath = downloadPath;
            match.mimeType = mimeType;
            totalDownloaded++;
          } else {
            console.log(`      ✗ Not an image (${mimeType})`);
            totalErrors++;
          }

          // Small delay
          await new Promise(resolve => setTimeout(resolve, 200));

        } catch (error) {
          console.log(`      ✗ Error: ${error.message}`);
          totalErrors++;
        }
      }

      results[projectSlug] = {
        ikropkaUrl: projectData.ikropkaUrl,
        imagesFound: imageUrls.length,
        matched: matches.length,
        matches
      };

    } catch (error) {
      console.log(`   ✗ Failed to scrape: ${error.message}`);
      totalErrors++;
    }

    // Delay between projects
    await new Promise(resolve => setTimeout(resolve, 500));
  }

  await browser.close();

  // Write results
  writeFileSync(OUTPUT_LOG, JSON.stringify(results, null, 2));

  console.log('\n' + '='.repeat(60));
  console.log('DOWNLOAD COMPLETE');
  console.log('='.repeat(60));
  console.log(`Projects processed: ${projects.length}`);
  console.log(`Images matched: ${totalMatched}`);
  console.log(`Downloaded: ${totalDownloaded}`);
  console.log(`Errors: ${totalErrors}`);
  console.log(`\nLog: ${OUTPUT_LOG}`);
}

main().catch(console.error);
