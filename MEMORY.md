# IKROPKA Migration Project Memory

**Last Updated:** 2026-07-16

---

## Active Decisions

### Language Support: Polish Only (Phase 1) — 2026-07-16
**Decision:** Build Polish-language site first, add multilingual support (EN, DE) in Phase 2
**Rationale:**
- Faster initial development
- Lower initial translation costs
- IKROPKA's primary market is Polish/local (Wrocław area)
- Can add languages later without rebuilding architecture
**Impact:**
- Phase 1 is Polish-only
- ROADMAP includes Phase 2 for AI-powered translation to EN/DE
- Translation glossary will be built during Phase 1 for future use

### Repository Privacy: Private Repo — 2026-07-16
**Decision:** GitHub repository will remain private
**Rationale:**
- GitHub Pages can host from private repos (requires paid account)
- Project is demo/preview only (GitHub Pages TOS prohibits commercial use)
- Keeps development and content private until ready
**Impact:**
- Need to ensure zamber's GitHub account supports private Pages (requires Pro/Team/Enterprise)
- Final production deployment will be on commercial hosting (Phase 3)

### Memory Separation: Project-Specific Memory — 2026-07-16
**Decision:** Keep ikropka-migration project memory separate from homelab infra notes
**Rationale:**
- Clear separation of concerns
- Infra notes in `/home/luna/projects/infra-notes/` (network, credentials, hosts)
- Project notes in `/home/luna/ikropka-migration/MEMORY.md` (content, design, decisions)
**Impact:**
- No mixing of infrastructure context with project context
- Each context system is self-contained and focused

---

## Content Mapping

### Source Site Analysis
**Status:** Complete (2026-07-16)
**Location:** `/home/luna/ikropka-migration/analysis/site-scrape.md`

**Key Stats:**
- **Total Pages:** 150+ (7 main nav + 14 offer subpages + 130+ portfolio projects)
- **Images:** 600+ across the site
- **Service Pages:** 14 detailed offer subpages
- **Portfolio Projects:** 130+ individual case studies
- **Interactive Elements:** Contact form (Contact Form 7), Google Maps, image sliders

### URL Structure (Old → New Mapping)

**Status:** TBD — will be defined during Jekyll setup

**Old Structure (WordPress):**
```
https://ikropka.eu/
https://ikropka.eu/o-nas/
https://ikropka.eu/oferty/
https://ikropka.eu/oferta/[service-slug]/
https://ikropka.eu/portfolio/
https://ikropka.eu/portfolio/[project-slug]/
https://ikropka.eu/referencje/
https://ikropka.eu/aktualnosci/
https://ikropka.eu/kontakt/
```

**New Structure (Jekyll):**
```
TBD — likely similar structure to preserve SEO:
/
/about/
/services/
/services/[service-slug]/
/portfolio/
/portfolio/[project-slug]/
/references/
/news/
/contact/
```

**Note:** Preserve URL structure where possible to minimize SEO impact. Use 301 redirects for any changes.

---

## Content Structure

### Content Types Identified

1. **Static Pages (7 main):**
   - Homepage (hero slider, featured projects, testimonials, contact form)
   - About (O nas) — company history, team, credentials, statistics
   - Services Hub (Oferta) — overview linking to 14 subpages
   - Portfolio (grid view with filtering)
   - References (testimonials, client logos)
   - News (Aktualności) — company updates
   - Contact (form, map, details)

2. **Service Subpages (14):**
   - Dendrology services (6): inventories, management plans, expert opinions, safety inspections, emergency services, tree protection
   - Design services (4): site development, green spaces, private gardens, parks/recreation
   - Supervision (1): green space inspector services
   - Historic objects (1): monument restoration projects
   - Consulting (1): advisory services
   - Training (1): workshops and courses

3. **Portfolio Projects (130+):**
   - Individual case study pages
   - Categories: Historic objects, Projects, Training
   - Each has: title, images, description, location, date

4. **Blog/News Posts:**
   - Company news and updates
   - Volume: TBD (needs scraping)

### Jekyll Collection Structure (Proposed)

```yaml
collections:
  services:
    output: true
    permalink: /oferta/:slug/
  portfolio:
    output: true
    permalink: /portfolio/:slug/
  posts:
    output: true
    permalink: /aktualnosci/:year/:month/:day/:slug/
```

**Status:** Proposed — needs finalization during Jekyll setup

---

## Technical Stack

### Current Status (2026-07-16)

**Source Site:**
- WordPress 6.1.10
- Custom theme "ik"
- Bootstrap 3.3.7
- jQuery 3.6.1
- LiteSpeed server
- Contact Form 7
- Google Maps integration

**Target Stack (Planned):**
- Jekyll 4.x (Ruby-based static site generator)
- Theme: TBD (awaiting user approval)
- Plugins:
  - jekyll-seo-tag (meta tags, Open Graph)
  - jekyll-sitemap (XML sitemap)
  - jekyll-feed (RSS feed)
  - jekyll-paginate (portfolio pagination)
  - TBD: others as needed
- Contact Form: Formspree or similar (static-site compatible)
- Hosting: GitHub Pages (demo), then commercial hosting (Phase 3)

### AI Translation Setup (Future — Phase 2)

**Model Selection (In Progress):**
- OpenRouter API access available
- Candidate models:
  - **Kimi K2.5**: $0.375/1M input, $2.025/1M output (cost-effective for bulk translation)
  - **Kimi K2.6**: $0.66/1M input, $3.41/1M output (newer, more expensive)
  - Other options: TBD based on quality benchmarks

**Translation Strategy:**
- Phase 1: Build glossary of specialized landscape architecture terms
- Phase 2: Batch translate PL → EN, PL → DE using selected model
- Human QA review after AI translation
- Use Jekyll i18n plugin for multilingual support

---

## Design Decisions

**Status:** Not yet started — awaiting Jekyll theme selection

**Requirements:**
- Mobile-first, responsive design
- SEO-optimized (fast load times, optimized images)
- Modern aesthetic (upgrade from Bootstrap 3.3.7)
- Minimal custom JavaScript (prefer CSS solutions)
- Hero slider on homepage
- Testimonial carousel
- Portfolio grid with filtering
- Contact form with GDPR compliance

**To Be Decided:**
- Color scheme (preserve IKROPKA branding?)
- Typography
- Layout/spacing
- Component library (Bootstrap 5, Tailwind, custom?)

---

## Open Questions

### Theme Selection — 2026-07-16
**Question:** Which Jekyll theme to use?
**Options:**
- Minimal Mistakes (feature-rich, highly customizable)
- Beautiful Jekyll (simple, clean)
- Jekyll Business (business-oriented)
- Agency Jekyll Theme (portfolio-focused)
- Custom theme

**Status:** Awaiting user feedback

**Factors to Consider:**
- SEO optimization out of the box
- Mobile responsiveness
- Portfolio/project showcase support
- Contact form integration
- Documentation quality
- Active maintenance
- Customization ease

### Portfolio Organization — 2026-07-16
**Question:** How to handle 130+ portfolio projects?
**Options:**
- Paginated grid (20-30 per page)
- Category filtering (Historic, Projects, Training)
- Infinite scroll
- Combination: filter + pagination

**Status:** Awaiting user feedback

### Image Optimization Strategy — 2026-07-16
**Question:** How to handle 600+ images?
**Considerations:**
- GitHub repo size limits
- CDN for performance?
- WebP conversion for smaller file sizes
- Lazy loading for performance

**Status:** Start with GitHub repo, optimize images heavily, revisit if repo size becomes an issue

---

## Future Enhancements (Roadmap)

See `ROADMAP.md` for full details.

**Phase 2: Multilingual Support (EN, DE)**
- AI-powered translation using OpenRouter
- Jekyll i18n plugin
- Language switcher UI
- Localized SEO

**Phase 3: Production Deployment**
- Commercial hosting (non-GitHub Pages)
- Custom domain
- 301 redirects from old site
- Final SEO audit

**Phase 4: Enhancements**
- Advanced portfolio filtering
- Search functionality
- Analytics integration
- Newsletter signup
- CRM integration (if needed)

---

## Translation Glossary (Building for Phase 2)

**Specialized Terms (Landscape Architecture / Dendrology):**

| Polish | English | German | Notes |
|--------|---------|--------|-------|
| inwentaryzacja dendrologiczna | tree inventory | Bauminventur | |
| operat dendrologiczny | dendrology management plan | dendrologischer Managementplan | |
| dendrolog | dendrologist | Dendrologe | |
| ekspertyza | expert assessment | Gutachten | |
| przegląd drzew | tree inspection | Baumkontrolle | |
| pogotowie dendrologiczne | emergency dendrology service | Baum-Notdienst | |
| projekt zagospodarowania terenu | site development project | Geländeerschließungsprojekt | |
| zieleń | green space / vegetation | Grünfläche | |
| architektura krajobrazu | landscape architecture | Landschaftsarchitektur | |
| obiekt zabytkowy | historic monument | Baudenkmal | |
| nadzór inspektora zieleni | green space inspector supervision | Grünflächeninspektoraufsicht | |

**Status:** Initial entries — will expand during content structuring

---

## Notes & Reminders

### For Claude
- Always update this file after making significant decisions
- Record URL mappings as they're finalized
- Build translation glossary as content is processed
- Document any deviations from the plan
- Keep infrastructure notes OUT of this file (belongs in `/home/luna/projects/infra-notes/`)

### For Project Team
- This is a living document — check before starting any phase
- ROADMAP.md has the high-level plan
- CLAUDE.md has the project guidance and conventions
- Analysis data in `analysis/` directory is the source of truth for old site structure

---

**Next Update Trigger:** After theme selection and Jekyll scaffolding
## Theme Decision - 2026-07-16

**Decision:** Minimal Mistakes theme selected
**Rationale:**
- Active maintenance (12k+ GitHub stars, frequent updates)
- Excellent SEO support built-in (jekyll-seo-tag)
- Highly customizable via _config.yml
- Strong documentation at https://mmistakes.github.io/minimal-mistakes/
- Portfolio/gallery support
- Mobile-first responsive design

**Trade-offs:**
- Requires more customization for business/agency look (but worth it for stability)
- Not as visually 'business-oriented' out of box, but very flexible

**Impact:**
- Will use Minimal Mistakes as base theme
- Customize for IKROPKA branding (colors, fonts, layouts)
- Leverage built-in portfolio/collection support for 130+ projects

## Portfolio Organization Decision - 2026-07-16

**Decision:** Category pages with optional pagination + lazy-loaded images + fuzzy search

**Architecture:**
- **Index page** (`/portfolio/`) - wszystkie 130+ projektów na jednej stronie
  - Lazy loading obrazków (tylko w viewport)
  - Przyciski kategorii → linkują do dedykowanych stron kategorii
  - Fuzzy search (fuse.js) po tytułach/opisach projektów
  - NO pagination initially (dodamy tylko jeżeli będą problemy z performance)

- **Category pages** (`/portfolio/zabytkowe/`, `/portfolio/projekty/`, `/portfolio/szkolenia/`)
  - Osobne strony dla każdej kategorii
  - Lazy loading obrazków
  - Fuzzy search na danej kategorii (fuse.js)
  - Paginacja opcjonalna (dodamy jeżeli potrzeba)

**Rationale:**
- Przyciski kategorii jako linki (nie client-side filtering) = lepsze SEO, czyste URLs
- Lazy loading obrazków rozwiązuje problem load times (nie content)
- 130 projektów tekstowo to niewiele danych — spokojnie można wylistować wszystkie
- Fuzzy search (fuse.js) dodaje świetny UX bez backend'u
- Paginacja "na zapas" tylko jeżeli performance wymusi

**Technical Implementation:**
- Jekyll collections dla portfolio (`_portfolio/`)
- Category filtering via front matter (`category: zabytkowe`)
- Lazy loading: Intersection Observer API lub `loading="lazy"` attribute
- Fuse.js dla search (lightweight, client-side, ~10KB gzipped)

**Impact:**
- Prostsze niż full client-side filtering z ładowaniem wszystkiego
- Lepsze SEO niż pure JS filtering
- Search dodaje discovery value
- Elastic — możemy dodać paginację później bez przepisywania


## Contact Form Decision - 2026-07-16

**Decision:** Deferred to later phase (TBD)

**Rationale:**
- Focus on content migration and structure first
- Form can be added anytime after core site is built
- Not blocking for demo/preview

**Phase 1 Approach:**
- Static contact page with email/phone/address info
- Placeholder text: "Formularz kontaktowy będzie dostępny wkrótce"
- Or: Simple mailto: link as temporary solution

**Phase 2/3 Implementation:**
- TBD: Formspree, Netlify Forms, or custom backend
- Requirements: file uploads, GDPR compliance, spam protection
- Will decide based on hosting platform chosen in Phase 3

**Impact:**
- Unblocks content migration work
- Allows focus on Jekyll setup and content structuring now


## Image Handling Strategy - 2026-07-16

**Decision:** Automatic download + optimization + WordPress thumbnail deduplication

**Approach:**
1. **Download all images** from ikropka.eu
2. **Deduplicate WordPress thumbnails** — WordPress creates multiple sizes (e.g., `-300x200.jpg`, `-1024x768.jpg`) from same source image
   - Detect by filename pattern (same base ID/slug)
   - Keep only largest/original version
   - Discard auto-generated thumbnails
3. **Optimize images:**
   - Convert to WebP (25-35% smaller than JPEG)
   - Compress to 80-85% quality
   - Fallback JPEG for compatibility
   - Max width: ~1200-1600px (sufficient for modern displays)
4. **Store in repo** (`site/assets/images/`)
   - Start simple — everything in Git
   - If repo size >500MB, migrate to CDN in Phase 2/3

**WordPress Thumbnail Deduplication Logic:**
- WordPress generates: `image.jpg`, `image-150x150.jpg`, `image-300x200.jpg`, `image-1024x768.jpg`
- Strategy: Group by base filename, keep largest dimension version only
- This should reduce 600+ images significantly

**Technical Implementation:**
- Script: `/home/luna/ikropka-migration/scripts/download-and-optimize-images.sh`
- Tools: `wget`/`curl` for download, `cwebp` for WebP conversion, `imagemagick`/`sharp` for optimization
- Output: `scraped-content/images/` (originals) → `site/assets/images/` (optimized)

**Impact:**
- Significantly reduces repo size by deduplicating WP thumbnails
- WebP saves 25-35% file size
- One automated script handles entire image migration


## Content Structuring AI Model Decision - 2026-07-16

**Decision:** Kimi K2.5 with incremental refinement approach

**Model Choice:**
- **Kimi K2.5** ($0.375/1M input, $2.025/1M output, 262K context)
- Estimated cost for 150 pages: ~$0.89 total
- Good structured output quality, handles long context well

**Approach: Refinement Loop (Critical for Success)**

**Phase 1: Initial Refinement (5 diverse test pages)**
1. Select 5 representative pages covering different complexity levels:
   - Homepage (hero slider, testimonials, mixed content)
   - Simple static page (e.g., About / O nas)
   - Service detail page (e.g., one oferta subpage - complex structure)
   - Portfolio project page (images, metadata)
   - News/blog post (if applicable)

2. For each page:
   - Run HTML → YAML conversion
   - **Manually review output quality**
   - Identify issues: missing fields, incorrect structure, malformed YAML
   - **Refine prompt** to handle edge cases
   - Re-run until output is clean

3. Document YAML schema and prompt in `/home/luna/ikropka-migration/scripts/content-extraction-prompt.md`

4. **Success criteria:** Zero manual fixes needed for test pages — YAML validates and maps cleanly to Jekyll

**Phase 2: Batch Processing (remaining ~145 pages)**
- Only proceed after refinement loop succeeds
- Use finalized prompt on all remaining pages
- Spot-check 10-20 random outputs for quality
- Fix any outliers

**YAML Schema Requirements:**

The conversion script must clearly define:
- **Standard fields:** title, description, layout, permalink, date, categories, tags
- **Custom fields:** portfolio metadata (client, location, year), service details, image arrays
- **Component handling:** How to represent sliders, galleries, testimonials, forms
- **Fallbacks:** What to do with unrecognized HTML elements (preserve as HTML block? Skip? Flag for manual review?)

**Non-standard Elements Strategy:**
- Custom WordPress shortcodes → Map to Jekyll includes or Liquid tags
- Embedded videos/iframes → Preserve with proper frontmatter metadata
- Contact forms → Placeholder comment in YAML
- Gallery blocks → Array of image objects with captions

**Technical Implementation:**
- Script: `/home/luna/ikropka-migration/scripts/extract-content-with-ai.js` (or .py)
- Prompt template: `/home/luna/ikropka-migration/scripts/content-extraction-prompt.md`
- OpenRouter API key: Check `~/.openclaw/workspace/bw_config.sh` or env vars
- Output: `/home/luna/ikropka-migration/content-structured/[page-slug].yaml`

**Impact:**
- Initial refinement loop (5 pages) is CRITICAL — don't rush this
- Well-defined schema prevents garbage-in-garbage-out
- Clean YAML = easy Jekyll integration
- Investment in prompt quality pays off for 150 pages


## Phase 1 Approval - 2026-07-16

**Timeline:** Approved — 3-4 weeks acceptable
**Branding:** Extract from current ikropka.eu site (colors, fonts, logo)
**Content Migration:** Can be phased — structure/scaffolding is priority, actual content migration can follow incrementally
**QA/Review:** User initially, then client later

**Critical Instruction from User:**
**NEVER defer/postpone planned tasks without explicit approval.** If a step seems long/problematic, ask for confirmation, but NEVER skip with a note "to be done later" — those tasks never get revisited and create confusion. Execute the plan fully or get explicit approval to modify scope.

This applies to:
- Planned features in milestones
- Scripts that should be written
- Content that should be migrated
- Any deliverable in the execution plan

If blocked or need to change approach: ASK, don't assume deferral is OK.


---

## Milestone 2 Complete - 2026-07-16

**Status:** ✅ COMPLETE

**Deliverables:**
- Jekyll 4.4.1 installed (Ruby 3.1.2)
- Minimal Mistakes 4.28.0 theme configured
- `_config.yml` configured with IKROPKA details:
  - Site title, description, locale (pl-PL)
  - Collections: portfolio, services
  - Plugins: SEO, sitemap, feed, paginate
  - Navigation structure
- Directory structure created: `_pages/`, `_portfolio/`, `_services/`, `_data/`, `assets/`
- Navigation configured (`_data/navigation.yml`) - main menu + sidebars
- Placeholder pages created: homepage (splash layout), about, services hub, portfolio, contact
- Local development server tested: ✅ http://localhost:4000/ikropka-migration/
- Build successful (warnings are deprecations from Sass, not errors)

**Technical Notes:**
- baseurl: `/ikropka-migration` (for GitHub Pages)
- Collections permalink structure:
  - Portfolio: `/portfolio/:slug/`
  - Services: `/oferta/:slug/`
- Sass deprecation warnings are normal (Minimal Mistakes uses older Sass syntax)

**Next:** Milestone 3 — Image Migration & Optimization


---

## Milestone 3 Progress - 2026-07-16

**Status:** 🔄 IN PROGRESS

### Scripts Created:

1. **`scripts/extract-image-urls-from-html.sh`** ✅
   - Extracts image URLs from downloaded HTML files
   - Handles relative and absolute URLs
   - Converts all to absolute https://ikropka.eu/ format

2. **`scripts/scrape-images-from-live-site.sh`** ✅
   - Uses wget to download HTML pages (level 3 recursion)
   - Extracted 26 image URLs from homepage initially

3. **`scripts/download-all-images-direct.sh`** ✅ (RUNNING)
   - Full site mirror with wget (downloads ALL images)
   - Accepts: jpg, jpeg, png, gif, webp, svg
   - Waits between requests (polite scraping)
   - Flattens directory structure after download
   - Currently running in background...

4. **`scripts/deduplicate-wp-thumbnails.js`** ✅
   - Node.js script to deduplicate WordPress thumbnails
   - Groups by base filename
   - Keeps largest version only
   - Ready to run after download completes

5. **`scripts/optimize-images.sh`** ✅
   - ImageMagick + cwebp for optimization
   - Converts to WebP (85% quality)
   - Creates JPEG fallback (85% quality)
   - Max width: 1600px
   - Strips metadata
   - Ready to run after deduplication

### Tools Installed:
- ImageMagick 6.9.11-60 ✅
- WebP tools (cwebp) ✅
- wget (already available) ✅

### Current Status: ✅ COMPLETE

**Final Stats:**
- **Downloaded:** 364 files via WordPress REST API (88MB original)
- **Deduplicated:** 349 unique images (no WordPress thumbnail duplicates found)
- **Optimized:** 696 output files (348 WebP + 348 JPEG = 696 total, 101MB)
- **Zero errors** during processing
- **Location:** `/home/luna/ikropka-migration/site/assets/images/`

**Download Approach:**
- WordPress REST API (`/wp-json/wp/v2/media`) proved most reliable
- Python script with requests library (paginated, 100 items per page)
- Shell scripts with wget failed (zero-byte files)

**Deduplication Results:**
- No WordPress thumbnails found (all 349 images were unique)
- Expected WordPress patterns like `-300x200.jpg` not present in downloads
- Source images were already deduplicated by API endpoint

**Optimization Details:**
- ImageMagick convert: JPEG fallback at 85% quality, max 1600px width, stripped metadata
- cwebp: WebP conversion at 85% quality
- Both formats for browser compatibility (`<picture>` element support)
- Output size slightly larger (101MB vs 70MB) due to dual-format strategy

**Next:** Commit milestone completion and begin Milestone 4 (Content Extraction).

