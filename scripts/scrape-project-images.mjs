#!/usr/bin/env node
/**
 * Scrape images directly from ikropka.eu project pages
 * Match by position in gallery (1:1 mapping)
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { basename } from 'path';

const BROKEN_IMAGES = 'broken-referenced-images.json';
const PORTFOLIO_DIR = 'docs/_portfolio';
const OUTPUT = 'direct-image-mapping.json';

console.log('=== Direct Source Scraping Strategy ===\n');

// Load broken images
const brokenImages = JSON.parse(readFileSync(BROKEN_IMAGES, 'utf-8'));

// Group by project
const brokenByProject = {};
for (const [imagePath, data] of Object.entries(brokenImages)) {
  const project = imagePath.split('/')[4];
  if (!brokenByProject[project]) {
    brokenByProject[project] = [];
  }
  brokenByProject[project].push({
    imagePath,
    filename: basename(imagePath),
    posts: data.posts
  });
}

console.log(`Found broken images in ${Object.keys(brokenByProject).length} projects\n`);

// For each project, read the post to understand image order
const projectMappings = {};

for (const [project, brokenImages] of Object.entries(brokenByProject)) {
  console.log(`\n📁 ${project} (${brokenImages.length} broken)`);

  // Find the markdown file
  const postFile = `${PORTFOLIO_DIR}/${project}.md`;
  if (!existsSync(postFile)) {
    console.log(`  ⚠ No post file found: ${postFile}`);
    continue;
  }

  // Read post frontmatter
  const content = readFileSync(postFile, 'utf-8');
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) {
    console.log(`  ⚠ No frontmatter in ${postFile}`);
    continue;
  }

  const frontmatter = frontmatterMatch[1];

  // Extract all image references IN ORDER
  const imageRefs = [];

  // Featured image first
  const featuredMatch = frontmatter.match(/featured_image:\s*(.+)/);
  if (featuredMatch) {
    imageRefs.push({
      path: featuredMatch[1].trim(),
      type: 'featured',
      filename: basename(featuredMatch[1].trim())
    });
  }

  // Gallery images in order
  const gallerySection = frontmatter.match(/gallery:([\s\S]*?)(?=\n\w+:|$)/);
  if (gallerySection) {
    const imagePathMatches = gallerySection[1].matchAll(/image_path:\s*(.+)/g);
    for (const match of imagePathMatches) {
      imageRefs.push({
        path: match[1].trim(),
        type: 'gallery',
        filename: basename(match[1].trim())
      });
    }
  }

  console.log(`  Found ${imageRefs.length} total image references`);

  // Check which are broken (HTML)
  const brokenRefs = [];
  for (let i = 0; i < imageRefs.length; i++) {
    const ref = imageRefs[i];
    const filePath = ref.path.startsWith('/') ? ref.path.substring(1) : ref.path;
    const fullPath = `docs/${filePath}`;

    if (!existsSync(fullPath)) {
      console.log(`  ⚠ Missing: ${ref.filename}`);
      continue;
    }

    try {
      const mimeType = execSync(`file --mime-type -b "${fullPath}"`, { encoding: 'utf-8' }).trim();
      if (mimeType === 'text/html') {
        brokenRefs.push({
          ...ref,
          position: i,
          fullPath
        });
      }
    } catch (e) {}
  }

  if (brokenRefs.length > 0) {
    projectMappings[project] = {
      slug: project,
      ikropkaUrl: `https://ikropka.eu/projekt/${project}/`,
      totalImages: imageRefs.length,
      brokenCount: brokenRefs.length,
      brokenImages: brokenRefs,
      allImages: imageRefs
    };

    console.log(`  ✗ ${brokenRefs.length} broken (positions: ${brokenRefs.map(r => r.position).join(', ')})`);
    console.log(`  → Will scrape: https://ikropka.eu/projekt/${project}/`);
  } else {
    console.log(`  ✓ All images working`);
  }
}

// Write mapping
writeFileSync(OUTPUT, JSON.stringify(projectMappings, null, 2));

console.log('\n=== Mapping Complete ===');
console.log(`Projects with broken images: ${Object.keys(projectMappings).length}`);
console.log(`Output: ${OUTPUT}`);

// Show projects to scrape
console.log('\nProjects to scrape:');
Object.entries(projectMappings)
  .sort((a, b) => b[1].brokenCount - a[1].brokenCount)
  .slice(0, 10)
  .forEach(([project, data]) => {
    console.log(`  ${project}: ${data.brokenCount} broken → ${data.ikropkaUrl}`);
  });
