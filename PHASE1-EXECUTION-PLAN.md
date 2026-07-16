# Phase 1 Execution Plan — IKROPKA Migration

**Project:** ikropka.eu → Jekyll static site
**Phase:** 1 — Foundation & Polish Site
**Status:** Awaiting User Approval
**Created:** 2026-07-16

---

## Executive Summary

This document outlines the complete execution plan for Phase 1 of the IKROPKA website migration. Phase 1 focuses on building a complete, SEO-optimized Polish-language Jekyll site with all content, images, and functionality migrated from the WordPress source.

**Key Decisions Made:**
- ✅ Jekyll theme: **Minimal Mistakes**
- ✅ Language: **Polish only** (EN/DE in Phase 2)
- ✅ Portfolio: **Category pages + lazy loading + fuzzy search** (fuse.js)
- ✅ Contact form: **Deferred to later phase** (TBD)
- ✅ Images: **Auto-download + optimize + deduplicate** → store in repo
- ✅ Content extraction: **Kimi K2.5 with 5-page refinement loop** before batch processing
- ✅ Repository: **Private GitHub repo** (github.com/zamber/ikropka-migration)

**Estimated Timeline:** 2-3 weeks (depending on content QA effort)
**Estimated AI Cost:** ~$0.89 (Kimi K2.5 for 150 pages)

---

## Phase 1 Milestones

### Milestone 1: Project Foundation ✅ COMPLETE
- [x] Create project directory structure
- [x] Initialize Git repository
- [x] Create GitHub private repository
- [x] Write CLAUDE.md (project guidance)
- [x] Write ROADMAP.md (multi-phase plan)
- [x] Write MEMORY.md (decisions log)
- [x] Complete site analysis (analysis/site-scrape.md)

**Status:** ✅ Done — repo at https://github.com/zamber/ikropka-migration

---

### Milestone 2: Jekyll Scaffolding & Theme Setup

**Goal:** Set up Jekyll project with Minimal Mistakes theme, configure for IKROPKA branding.

#### Tasks:

**2.1 Install Jekyll and Dependencies**
```bash
cd /home/luna/ikropka-migration
mkdir site
cd site
gem install bundler jekyll
jekyll new . --skip-bundle
```

**2.2 Install Minimal Mistakes Theme**

Add to `Gemfile`:
```ruby
gem "minimal-mistakes-jekyll"
gem "jekyll-include-cache"
gem "jekyll-seo-tag"
gem "jekyll-sitemap"
gem "jekyll-feed"
gem "jekyll-paginate"
```

Run:
```bash
bundle install
```

**2.3 Configure `_config.yml`**

Key settings:
- Site title: "IKROPKA — Pracownia Architektury Krajobrazu"
- Description: SEO-optimized site description
- URL: TBD (GitHub Pages URL for now)
- Theme: minimal-mistakes
- Locale: pl-PL
- Collections: portfolio, services
- Plugins: SEO, sitemap, feed, paginate

**2.4 Create Directory Structure**
```
site/
├── _config.yml
├── _data/
│   └── navigation.yml (menu structure)
├── _pages/
│   ├── index.md (homepage)
│   ├── about.md (o-nas)
│   ├── services.md (oferta hub)
│   ├── portfolio.md (portfolio index)
│   ├── references.md (referencje)
│   ├── news.md (aktualności)
│   └── contact.md (kontakt - static for now)
├── _portfolio/ (collection for 130+ projects)
├── _services/ (collection for 14 service pages)
├── _posts/ (blog/news posts)
├── assets/
│   ├── images/
│   ├── css/
│   └── js/
├── _includes/ (custom components)
└── _layouts/ (custom layouts if needed)
```

**2.5 Test Local Development Environment**
```bash
bundle exec jekyll serve
# Visit http://localhost:4000
```

**Success Criteria:**
- Jekyll site builds without errors
- Minimal Mistakes theme loads correctly
- Navigation structure in place
- Placeholder content on main pages

**Estimated Time:** 1-2 days

---

### Milestone 3: Image Migration & Optimization

**Goal:** Download all images from ikropka.eu, deduplicate WordPress thumbnails, optimize, and store in repo.

#### Tasks:

**3.1 Create Image Download Script**

Script: `/home/luna/ikropka-migration/scripts/download-images.sh`

Requirements:
- Parse `analysis/site-scrape.md` for all image URLs
- Download all images to `scraped-content/images/original/`
- Preserve directory structure or use meaningful naming

**3.2 Create Deduplication Script**

Script: `/home/luna/ikropka-migration/scripts/deduplicate-wp-thumbnails.js`

Logic:
- Identify WordPress thumbnail patterns: `image-{width}x{height}.jpg`
- Group by base filename
- Keep only largest dimension version
- Output: `scraped-content/images/deduplicated/`

Example:
```
Input:
  photo-123.jpg (2000x1500)
  photo-123-1024x768.jpg
  photo-123-300x200.jpg
  photo-123-150x150.jpg

Output:
  photo-123.jpg (2000x1500) ← keep this only
```

**3.3 Create Optimization Script**

Script: `/home/luna/ikropka-migration/scripts/optimize-images.sh`

Requirements:
- **Convert to WebP** (85% quality)
- **Generate JPEG fallback** (85% quality, max 1600px width)
- Use tools: `cwebp`, `imagemagick` (convert), or `sharp` (Node.js)
- Output: `site/assets/images/`

Structure:
```
site/assets/images/
├── portfolio/
│   ├── project-slug/
│   │   ├── image1.webp
│   │   ├── image1.jpg (fallback)
│   │   ├── image2.webp
│   │   └── image2.jpg
├── services/
├── about/
└── general/
```

**3.4 Run Full Pipeline**
```bash
cd /home/luna/ikropka-migration
./scripts/download-images.sh
./scripts/deduplicate-wp-thumbnails.js
./scripts/optimize-images.sh
```

**3.5 Verify Output**
- Count: ~600 original → after deduplication → after optimization
- Check file sizes (WebP should be 25-35% smaller than JPEG)
- Spot-check image quality
- Commit to Git (if repo size < 500MB, proceed; if >500MB, re-evaluate CDN)

**Success Criteria:**
- All unique images downloaded and optimized
- WebP + JPEG fallbacks generated
- Images organized by content type (portfolio, services, etc.)
- Total repo size manageable (<500MB)

**Estimated Time:** 2-3 days (includes script development + processing time)

---

### Milestone 4: Content Extraction — Refinement Loop (CRITICAL)

**Goal:** Develop and refine AI-powered HTML → YAML extraction pipeline using Kimi K2.5.

**⚠️ This is the most critical milestone** — invest time here to ensure quality.

#### Tasks:

**4.1 Select 5 Representative Test Pages**

Choose diverse pages:
1. **Homepage** — https://ikropka.eu/ (complex: hero slider, testimonials, mixed sections)
2. **About page** — https://ikropka.eu/o-nas/ (static content, team info, stats)
3. **Service detail** — https://ikropka.eu/oferta/inwentaryzacje-dendrologiczne/ (structured service page)
4. **Portfolio project** — Pick one from https://ikropka.eu/portfolio/ (images, metadata)
5. **News/Blog post** — One from https://ikropka.eu/aktualnosci/ (if content exists)

**4.2 Define YAML Schema**

Document: `/home/luna/ikropka-migration/scripts/yaml-schema.md`

Example schema for different page types:

**Homepage YAML:**
```yaml
---
layout: home
title: "IKROPKA — Pracownia Architektury Krajobrazu"
description: "Landscape architecture services in Wrocław..."
permalink: /

hero:
  slides:
    - image: /assets/images/hero-1.jpg
      alt: "Description"
      caption: "Optional caption"
      cta_text: "Call to action"
      cta_url: "/oferta/"

sections:
  - type: intro
    heading: "O nas"
    content: |
      Multi-line content...

  - type: strengths
    items:
      - icon: "tree"
        title: "Doświadczenie"
        description: "..."
      - icon: "design"
        title: "Projekty"
        description: "..."

  - type: featured_projects
    heading: "Wybrane projekty"
    projects:
      - slug: "project-slug-1"
      - slug: "project-slug-2"

  - type: testimonials
    items:
      - author: "Jan Kowalski"
        company: "Firma XYZ"
        content: "Quote..."
      - author: "Anna Nowak"
        company: "Instytucja ABC"
        content: "Quote..."

  - type: contact_form
    note: "Placeholder — form deferred to Phase 2/3"
---
```

**Service Page YAML:**
```yaml
---
layout: service
title: "Inwentaryzacje Dendrologiczne"
description: "Professional tree inventory services..."
permalink: /oferta/inwentaryzacje-dendrologiczne/
category: services
service_type: dendrology

hero_image: /assets/images/services/inwentaryzacje-hero.jpg

sections:
  - type: intro
    content: |
      Description of the service...

  - type: features
    heading: "Co oferujemy"
    items:
      - "Feature 1"
      - "Feature 2"
      - "Feature 3"

  - type: process
    heading: "Proces realizacji"
    steps:
      - number: 1
        title: "Wizja lokalna"
        description: "..."
      - number: 2
        title: "Dokumentacja"
        description: "..."

  - type: cta
    text: "Skontaktuj się z nami"
    button_text: "Kontakt"
    button_url: "/kontakt/"

related_services:
  - slug: "operat-dendrologiczny"
  - slug: "dendrolog-opinie-ekspertyzy"
---
```

**Portfolio Project YAML:**
```yaml
---
layout: portfolio_single
title: "Park miejski w Oleśnicy"
description: "Project description..."
permalink: /portfolio/park-miejski-olesnica/
category: projekty # or: zabytkowe, szkolenia

project_meta:
  client: "Gmina Oleśnica"
  location: "Oleśnica, woj. dolnośląskie"
  year: 2019
  scope: "Projekt zagospodarowania terenu"
  area: "2.5 ha"

gallery:
  - image: /assets/images/portfolio/olesnica/photo1.jpg
    alt: "Description"
    caption: "Optional caption"
  - image: /assets/images/portfolio/olesnica/photo2.jpg
    alt: "Description"

sections:
  - type: description
    content: |
      Multi-paragraph project description...

  - type: challenges
    heading: "Wyzwania"
    content: "..."

  - type: solution
    heading: "Rozwiązania"
    content: "..."

tags:
  - park
  - rekreacja
  - zieleń miejska
---
```

**4.3 Create AI Extraction Script**

Script: `/home/luna/ikropka-migration/scripts/extract-content.js` (Node.js) or `.py` (Python)

Requirements:
- Load HTML from scraped page
- Send to OpenRouter (Kimi K2.5) with detailed prompt
- Parse JSON/YAML response
- Validate YAML syntax
- Save to `content-structured/[page-slug].yaml`

**Prompt Template** (`scripts/content-extraction-prompt.md`):
```markdown
You are an expert at extracting structured data from HTML.

TASK: Convert the following WordPress HTML page into a clean YAML structure for Jekyll.

YAML SCHEMA:
[Insert appropriate schema from yaml-schema.md based on page type]

INSTRUCTIONS:
1. Extract all semantic content (headings, paragraphs, lists, images)
2. Identify content sections and their types
3. Extract metadata (title, description, dates, categories)
4. Handle images: extract src, alt, captions
5. Handle special components:
   - Sliders → array of slides
   - Testimonials → array of testimonial objects
   - Forms → note as placeholder (deferred to Phase 2)
   - Galleries → array of images with metadata
6. Preserve content hierarchy
7. Use multi-line YAML strings (|) for long text
8. Ensure valid YAML syntax (proper indentation, quoted strings when needed)

EDGE CASES:
- If unrecognized HTML element → preserve as `html_block` with raw HTML
- If embedded video/iframe → extract to `embed` field with URL and type
- If WordPress shortcode → document in `custom_elements` array

OUTPUT FORMAT: Valid YAML only. No explanations, no markdown code blocks.

HTML INPUT:
[paste HTML here]

YAML OUTPUT:
```

**4.4 Refinement Loop (5 Test Pages)**

For each test page:
1. Run extraction script
2. **Manually review YAML output**:
   - Is structure correct?
   - Are all important elements captured?
   - Is YAML valid? (use `yamllint` or online validator)
   - Does it map cleanly to Jekyll expectations?
3. **Identify issues**:
   - Missing fields?
   - Incorrect nesting?
   - Malformed YAML?
   - Lost content?
4. **Refine prompt**:
   - Add specific instructions for identified issues
   - Update schema if needed
   - Add examples to prompt
5. **Re-run extraction**
6. **Repeat until clean** — no manual fixes needed

**Success Criteria (MUST MEET BEFORE PROCEEDING):**
- ✅ All 5 test pages extract cleanly
- ✅ YAML validates without errors
- ✅ No content loss (all important elements captured)
- ✅ Structure matches schema expectations
- ✅ Ready for Jekyll integration without manual editing

**Estimated Time:** 3-5 days (iterative refinement is time-consuming but critical)

**4.5 Document Finalized Prompt**

Save to: `/home/luna/ikropka-migration/scripts/content-extraction-prompt-final.md`

Include:
- Full prompt text
- YAML schema definitions
- Examples of good output
- Edge case handling rules

---

### Milestone 5: Batch Content Extraction

**Goal:** Process remaining ~145 pages using refined extraction pipeline.

#### Tasks:

**5.1 Prepare Page List**

Create: `/home/luna/ikropka-migration/scripts/pages-to-process.json`

```json
[
  {
    "url": "https://ikropka.eu/",
    "type": "homepage",
    "output": "content-structured/homepage.yaml"
  },
  {
    "url": "https://ikropka.eu/o-nas/",
    "type": "about",
    "output": "content-structured/about.yaml"
  },
  {
    "url": "https://ikropka.eu/oferta/inwentaryzacje-dendrologiczne/",
    "type": "service",
    "output": "content-structured/services/inwentaryzacje-dendrologiczne.yaml"
  },
  ...
]
```

**5.2 Run Batch Processing**

```bash
cd /home/luna/ikropka-migration
./scripts/extract-content-batch.js
# Processes all pages in pages-to-process.json
# Rate limit: respect OpenRouter API limits
# Progress: log each page processed
# Errors: log to extraction-errors.log
```

**5.3 Quality Spot-Check**

- Randomly select 10-20 extracted YAML files
- Manually review for quality
- If issues found → refine prompt and re-run problematic pages
- Validate all YAML files: `find content-structured -name "*.yaml" -exec yamllint {} \;`

**5.4 Organize Structured Content**

Directory structure:
```
content-structured/
├── homepage.yaml
├── about.yaml
├── contact.yaml
├── services/
│   ├── inwentaryzacje-dendrologiczne.yaml
│   ├── operat-dendrologiczny.yaml
│   └── ... (14 total)
├── portfolio/
│   ├── project-slug-1.yaml
│   ├── project-slug-2.yaml
│   └── ... (130+ total)
└── posts/
    └── news-post-1.yaml
```

**Success Criteria:**
- All 150+ pages processed
- YAML files validate
- No critical content loss
- Organized by content type

**Estimated Time:** 2-3 days (includes processing + QA)
**Estimated Cost:** ~$0.89 (Kimi K2.5)

---

### Milestone 6: Jekyll Content Integration

**Goal:** Convert structured YAML to Jekyll markdown files with frontmatter.

#### Tasks:

**6.1 Create YAML → Jekyll Conversion Script**

Script: `/home/luna/ikropka-migration/scripts/yaml-to-jekyll.js`

Logic:
- Read YAML file from `content-structured/`
- Extract frontmatter fields → YAML frontmatter block
- Extract content sections → Markdown body (using Liquid tags/includes for components)
- Save to appropriate Jekyll directory:
  - Services → `site/_services/`
  - Portfolio → `site/_portfolio/`
  - Posts → `site/_posts/`
  - Pages → `site/_pages/`

**6.2 Create Custom Jekyll Includes for Components**

Create includes for special components:
- `_includes/hero-slider.html` (homepage slider)
- `_includes/testimonials-carousel.html`
- `_includes/portfolio-grid.html`
- `_includes/service-features.html`
- `_includes/contact-info.html`

Use Liquid templating to render from frontmatter data.

**6.3 Process All Content**

```bash
./scripts/yaml-to-jekyll.js --input content-structured --output site
```

**6.4 Build Jekyll Site**

```bash
cd site
bundle exec jekyll build
# Check for errors
# Fix any broken references, missing images, etc.
```

**6.5 Manual Review**

- Spot-check 10-20 pages on localhost:4000
- Verify:
  - Content displays correctly
  - Images load
  - Navigation works
  - Layouts render properly
  - No broken links

**Success Criteria:**
- Jekyll builds without errors
- All pages accessible
- Content matches original site (semantically)
- Images display correctly

**Estimated Time:** 3-4 days

---

### Milestone 7: Portfolio Features (Lazy Loading + Search)

**Goal:** Implement lazy loading for images and fuzzy search with fuse.js.

#### Tasks:

**7.1 Implement Lazy Loading**

Option A: Use native `loading="lazy"` attribute
```html
<img src="/assets/images/..." alt="..." loading="lazy">
```

Option B: Intersection Observer API (more control)
- Create `assets/js/lazy-load.js`
- Use Intersection Observer to load images when in viewport

**7.2 Implement Fuzzy Search (Fuse.js)**

**Install Fuse.js:**
- Download fuse.js (minified, ~10KB) to `site/assets/js/fuse.min.js`

**Create Search Index:**
- Generate JSON index of all portfolio projects: `site/assets/search-index.json`

```json
[
  {
    "title": "Park miejski w Oleśnicy",
    "description": "Project description...",
    "category": "projekty",
    "url": "/portfolio/park-miejski-olesnica/",
    "tags": ["park", "rekreacja"]
  },
  ...
]
```

**Create Search UI:**
- Add search input to `/portfolio/` page
- `assets/js/search.js` — init Fuse.js, handle search queries, filter results

**7.3 Category Pages**

Create three category pages:
- `site/_pages/portfolio-zabytkowe.md` → `/portfolio/zabytkowe/`
- `site/_pages/portfolio-projekty.md` → `/portfolio/projekty/`
- `site/_pages/portfolio-szkolenia.md` → `/portfolio/szkolenia/`

Each uses Liquid to filter `site.portfolio` by category frontmatter.

**7.4 Test**

- Test lazy loading (inspect network tab, images load on scroll)
- Test search (type query, results filter instantly)
- Test category pages (correct projects shown)

**Success Criteria:**
- Images lazy load properly
- Search works smoothly (fuzzy matching, fast)
- Category pages display correct projects

**Estimated Time:** 2-3 days

---

### Milestone 8: SEO Optimization

**Goal:** Ensure all pages have proper SEO elements (meta tags, structured data, sitemap, robots.txt).

#### Tasks:

**8.1 Configure jekyll-seo-tag**

Already included with Minimal Mistakes. Ensure in `_config.yml`:
```yaml
plugins:
  - jekyll-seo-tag

title: "IKROPKA — Pracownia Architektury Krajobrazu"
description: "..."
url: "https://zamber.github.io/ikropka-migration" # or custom domain later
author: "IKROPKA"
logo: "/assets/images/logo.png"
social:
  name: IKROPKA
  links:
    - https://facebook.com/...
```

Ensure every page has frontmatter:
```yaml
title: "Page Title (max 60 chars)"
description: "Meta description 150-160 chars..."
```

**8.2 Add Structured Data (JSON-LD)**

Create include: `_includes/structured-data.html`

**LocalBusiness schema (for site-wide footer):**
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "IKROPKA Pracownia Architektury Krajobrazu",
  "description": "...",
  "url": "https://ikropka.eu",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ul. Sudecka 74 lok. 2",
    "addressLocality": "Wrocław",
    "postalCode": "53-129",
    "addressCountry": "PL"
  },
  "telephone": "+48 600 181 389",
  "email": "biuro@ikropka.eu"
}
```

**Service schema (for each service page):**
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Inwentaryzacje Dendrologiczne",
  "description": "...",
  "provider": {
    "@type": "LocalBusiness",
    "name": "IKROPKA"
  }
}
```

**8.3 Generate XML Sitemap**

`jekyll-sitemap` plugin handles this automatically. Verify `site/sitemap.xml` is generated.

**8.4 Create robots.txt**

`site/robots.txt`:
```
User-agent: *
Allow: /
Sitemap: https://zamber.github.io/ikropka-migration/sitemap.xml
```

**8.5 Add Open Graph & Twitter Card Tags**

`jekyll-seo-tag` handles this automatically if frontmatter includes:
```yaml
image: /assets/images/og-image.jpg # social share image
```

Create default OG image if pages don't have specific images.

**8.6 Performance Optimization**

- Minify CSS/JS (use Jekyll plugins or build tools)
- Optimize images (already done in Milestone 3)
- Enable compression (handled by GitHub Pages automatically)

**8.7 Run SEO Audit**

Tools:
- Google Lighthouse (built into Chrome DevTools)
- Run on key pages: homepage, service page, portfolio page

Target scores:
- Performance: 90+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

Fix any issues identified.

**Success Criteria:**
- All pages have unique titles and descriptions
- Structured data validates (use Google Rich Results Test)
- Sitemap.xml and robots.txt present
- Lighthouse scores meet targets

**Estimated Time:** 2-3 days

---

### Milestone 9: Design Customization

**Goal:** Customize Minimal Mistakes theme for IKROPKA branding.

#### Tasks:

**9.1 Define Brand Colors & Fonts**

Research current ikropka.eu:
- Primary color: (extract from site)
- Secondary color: (extract from site)
- Typography: (extract from site)

Document in `/home/luna/ikropka-migration/site/_sass/custom-variables.scss`

**9.2 Override Minimal Mistakes Styles**

Create: `site/_sass/custom.scss`

Customize:
- Header/navigation colors
- Button styles
- Typography (font families, sizes)
- Spacing/layout
- Footer styling

Import in `site/assets/css/main.scss`:
```scss
@import "minimal-mistakes/skins/default"; // or custom skin
@import "custom-variables";
@import "custom";
```

**9.3 Customize Layouts**

If needed, override Minimal Mistakes layouts:
- Copy layout from gem to `site/_layouts/`
- Customize HTML structure
- Preserve Liquid logic

**9.4 Add Logo and Favicon**

- Create/export logo: `site/assets/images/logo.png`
- Create favicon: `site/assets/images/favicon.ico` (and various sizes for devices)
- Configure in `_config.yml`:
  ```yaml
  logo: "/assets/images/logo.png"
  ```

**9.5 Hero Slider (Homepage)**

Implement custom hero slider (or use existing carousel library like Slick/Swiper).

Create: `_includes/hero-slider.html`

**9.6 Testimonials Carousel**

Create: `_includes/testimonials-carousel.html`

Use lightweight carousel library or custom CSS.

**9.7 Responsive Testing**

Test on:
- Desktop (1920px, 1366px)
- Tablet (768px, 1024px)
- Mobile (375px, 414px)

Fix any layout issues.

**Success Criteria:**
- Site visually aligned with IKROPKA branding
- Custom colors, fonts, logo applied
- Hero slider works smoothly
- Testimonials carousel functional
- Fully responsive on all devices

**Estimated Time:** 4-5 days

---

### Milestone 10: Final QA & GitHub Pages Deployment

**Goal:** Comprehensive testing, bug fixes, and deployment to GitHub Pages.

#### Tasks:

**10.1 Comprehensive Testing**

**Content QA:**
- [ ] All pages load correctly
- [ ] No broken links (use `jekyll-link-checker` or manual check)
- [ ] All images display
- [ ] Portfolio projects have correct metadata and images
- [ ] Service pages have complete content
- [ ] About page has team info and stats
- [ ] Contact page has correct info (email, phone, address, map)

**Functionality QA:**
- [ ] Navigation menu works (all links correct)
- [ ] Portfolio search works (fuzzy search functional)
- [ ] Category filtering works (correct projects shown)
- [ ] Lazy loading works (images load on scroll)
- [ ] Hero slider works (auto-play, manual controls)
- [ ] Testimonials carousel works

**SEO QA:**
- [ ] All pages have unique titles & descriptions
- [ ] Structured data validates
- [ ] Sitemap.xml accessible and correct
- [ ] robots.txt correct
- [ ] Lighthouse scores meet targets (90+ performance, 100 others)

**Responsive QA:**
- [ ] Test on desktop, tablet, mobile
- [ ] No layout breaks
- [ ] Touch-friendly navigation on mobile
- [ ] Images scale properly

**Cross-Browser QA:**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (if available)
- [ ] Edge (latest)

**10.2 Bug Fixes**

Create issue list: `site/BUGS.md`

Fix all critical and high-priority bugs.

**10.3 Final Content Review**

- Proofread key pages (homepage, about, services)
- Check for placeholder text or lorem ipsum
- Verify contact information is correct

**10.4 Configure GitHub Pages**

**In GitHub repo settings:**
1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: `main` (or `gh-pages` if using separate branch)
4. Folder: `/` (if Jekyll site is at repo root) or `/site` (if nested)

**Note:** If site is in `/site` subdirectory, you may need to:
- Move `site/*` to repo root, OR
- Use GitHub Actions to build from `site/` directory

**Update `_config.yml`:**
```yaml
url: "https://zamber.github.io"
baseurl: "/ikropka-migration"
```

**10.5 Deploy to GitHub Pages**

```bash
cd /home/luna/ikropka-migration/site
git add -A
git commit -m "feat: complete Phase 1 Jekyll site"
git push origin main
```

Wait for GitHub Pages to build (check Actions tab).

**10.6 Verify Deployment**

Visit: `https://zamber.github.io/ikropka-migration/`

- [ ] Site loads
- [ ] All pages accessible
- [ ] Images load (check paths with baseurl)
- [ ] No console errors
- [ ] Navigation works

**10.7 Document Known Issues**

Create: `site/KNOWN-ISSUES.md`

List any non-critical issues or Phase 2 improvements.

**Success Criteria:**
- Site fully functional on GitHub Pages
- No critical bugs
- SEO optimized
- Ready for stakeholder review

**Estimated Time:** 3-4 days

---

## Phase 1 Deliverables

Upon completion, Phase 1 delivers:

1. ✅ **Complete Jekyll site** with Minimal Mistakes theme
2. ✅ **All content migrated** (150+ pages)
3. ✅ **All images optimized** and deduplicated
4. ✅ **Portfolio with search and filtering** (130+ projects)
5. ✅ **14 service pages** fully detailed
6. ✅ **SEO optimized** (meta tags, structured data, sitemap)
7. ✅ **Mobile-responsive** design
8. ✅ **Deployed to GitHub Pages** for preview
9. ✅ **Documentation**:
   - CLAUDE.md (project guidance)
   - MEMORY.md (decisions log)
   - ROADMAP.md (multi-phase plan)
   - PHASE1-EXECUTION-PLAN.md (this document)
   - Scripts for content extraction, image optimization

---

## Phase 1 Timeline Estimate

| Milestone | Estimated Duration |
|-----------|-------------------|
| 1. Project Foundation | ✅ Complete |
| 2. Jekyll Scaffolding | 1-2 days |
| 3. Image Migration | 2-3 days |
| 4. Content Extraction (Refinement) | 3-5 days |
| 5. Batch Content Extraction | 2-3 days |
| 6. Jekyll Content Integration | 3-4 days |
| 7. Portfolio Features | 2-3 days |
| 8. SEO Optimization | 2-3 days |
| 9. Design Customization | 4-5 days |
| 10. Final QA & Deployment | 3-4 days |

**Total Estimated Timeline: 22-32 days (3-4.5 weeks)**

Note: Timeline assumes dedicated work. Adjust for interruptions, user feedback cycles, etc.

---

## Phase 1 Cost Estimate

| Item | Cost |
|------|------|
| Kimi K2.5 API (150 pages) | ~$0.89 |
| GitHub (already have paid account) | $0 |
| Tools (cwebp, imagemagick, etc.) | Free (open source) |

**Total Estimated Cost: ~$0.89**

---

## Phase 1 Success Metrics

At the end of Phase 1, the site must meet these criteria:

- [ ] **Content Completeness:** All 150+ pages migrated, no missing content
- [ ] **Image Quality:** All images optimized, no broken images
- [ ] **SEO:** Lighthouse scores 90+ performance, 100 accessibility/SEO/best-practices
- [ ] **Functionality:** Portfolio search works, lazy loading works, navigation works
- [ ] **Responsive:** Site works on desktop, tablet, mobile
- [ ] **Deployment:** Live on GitHub Pages, accessible to stakeholders
- [ ] **Documentation:** All decisions logged in MEMORY.md, roadmap clear

---

## Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Content extraction quality issues | High | Medium | 5-page refinement loop (Milestone 4) before batch |
| Repo size >1GB (GitHub limit) | Medium | Low | Aggressive image optimization + deduplication |
| Jekyll theme customization difficulty | Medium | Low | Minimal Mistakes is well-documented; fallback to simpler layouts if needed |
| GitHub Pages TOS (commercial use) | Low | N/A | Clearly marked as demo; Phase 3 moves to commercial hosting |
| Timeline slippage | Medium | Medium | Buffer time built into estimates; prioritize core features |

---

## Phase 1 → Phase 2 Transition

After Phase 1 completion and user approval:

**Phase 2 begins:** Multilingual support (EN, DE)
- AI translation pipeline (PL → EN, PL → DE)
- Jekyll i18n plugin integration
- Language switcher UI
- Localized SEO

See `ROADMAP.md` for Phase 2 details.

---

## Approval Checklist

Before proceeding with Phase 1 execution, confirm:

- [ ] **Theme choice approved:** Minimal Mistakes (confirmed)
- [ ] **Portfolio structure approved:** Category pages + lazy loading + search (confirmed)
- [ ] **Contact form deferral approved:** TBD in later phase (confirmed)
- [ ] **Image strategy approved:** Auto-download + optimize + deduplicate (confirmed)
- [ ] **AI model approved:** Kimi K2.5 with refinement loop (confirmed)
- [ ] **Timeline acceptable:** ~3-4 weeks (user review needed)
- [ ] **Budget acceptable:** ~$0.89 AI cost (user review needed)
- [ ] **Any additional requirements?** (user input needed)

---

## Next Steps After Approval

1. **User reviews and approves this plan**
2. **Begin Milestone 2:** Jekyll scaffolding setup
3. **Daily progress updates** committed to MEMORY.md
4. **Weekly check-ins** with user for feedback
5. **Proceed through milestones sequentially**

---

**Status:** ⏳ Awaiting User Approval

**Prepared by:** Claude Code Agent
**Date:** 2026-07-16

---

## Questions for User

Before I begin execution, please confirm:

1. **Is the ~3-4 week timeline acceptable?**
2. **Any specific branding requirements** (colors, fonts, logo) I should know about before Milestone 9?
3. **Any pages or content I should prioritize** if we need to phase the work?
4. **Who will review/QA** the site during development? (user, stakeholders, etc.)
5. **Anything missing from this plan?**

Once you approve, I'll begin with Milestone 2 (Jekyll Scaffolding). 🚀
