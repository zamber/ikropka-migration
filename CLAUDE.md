# CLAUDE.md - IKROPKA Migration Project

This file provides guidance to Claude Code when working on the IKROPKA website migration project.

## Project Overview

**Goal:** Migrate and modernize the IKROPKA.eu landscape architecture website from a custom WordPress theme to a modern, SEO-optimized Jekyll static site hosted on GitHub Pages.

**Source:** https://ikropka.eu/ (WordPress 6.1.10, custom "ik" theme, Bootstrap 3.3.7)
**Target:** Jekyll static site with modern theme, mobile-responsive, SEO-optimized

**Important:** This is a **demo/preview project only**. GitHub Pages TOS prohibits commercial use. Final deployment will be on commercial hosting (to be determined later).

---

## Project Memory Convention

### Memory Storage Location

Project-specific facts, decisions, and context should be stored in:
- **`/home/luna/ikropka-migration/MEMORY.md`** — Main project memory file
- **`/home/luna/ikropka-migration/memory/`** — Directory for topic-specific memory files

### What to Record

Record important facts about:
1. **Decisions made** — Architecture choices, theme selection, content structure decisions
2. **Content mapping** — How old URLs map to new structure
3. **SEO requirements** — Meta descriptions, keywords, redirects needed
4. **Translation glossary** — Key Polish→English/German terms for future multilingual support
5. **Design decisions** — Layout choices, color schemes, component decisions
6. **Technical constraints** — Jekyll limitations, plugin choices, GitHub Pages restrictions

### What NOT to Record Here

**DO NOT** mix infrastructure/homelab notes here. Those belong in:
- **`/home/luna/projects/infra-notes/INFRASTRUCTURE.md`** (homelab inventory, credentials)
- **`/home/luna/projects/infra-notes/CHANGELOG.md`** (infra changes log)

Keep project context separate from infrastructure context.

### Memory File Format

Use this format for `MEMORY.md`:

```markdown
# IKROPKA Migration Project Memory

Last updated: YYYY-MM-DD

## Active Decisions

### [Decision Title] — YYYY-MM-DD
**Decision:** What was decided
**Rationale:** Why this choice was made
**Impact:** What this affects

## Content Mapping

### URL Redirects
- Old URL → New URL mapping

### Content Structure
- How content is organized in Jekyll

## Technical Stack

### Current Status
- Jekyll version, theme, plugins in use

## Open Questions

### [Question] — YYYY-MM-DD
What needs to be decided/researched

## Future Enhancements (Roadmap)

- Multilingual support (EN, DE) using AI translation
- [Other planned features]
```

---

## Project Directory Structure

```
/home/luna/ikropka-migration/
├── CLAUDE.md              # This file (project guidance for Claude)
├── MEMORY.md              # Project memory (decisions, mappings)
├── ROADMAP.md             # Future enhancements and phases
├── README.md              # Human-readable project overview
├── analysis/              # Scraped site analysis
│   ├── site-scrape.md     # Complete source site analysis
│   ├── ANALYSIS-SUMMARY.md
│   └── portfolio-projects-full-list.txt
├── scraped-content/       # Downloaded images, pages, assets
├── content-structured/    # AI-translated structured data (JSON/YAML)
├── site/                  # Jekyll site root (git tracked, pushed to GitHub)
│   ├── _config.yml
│   ├── _posts/
│   ├── _pages/
│   ├── assets/
│   └── ...
└── memory/                # Topic-specific memory files
```

---

## GitHub Repository

**Repo:** `zamber/ikropka-migration` (private)
**Purpose:** Demo/preview only (GitHub Pages TOS compliance)
**GitHub Pages:** Yes, can be hosted from private repos (requires paid GitHub account or public repo)
**Branch:** `main` (default branch, deployed to Pages)

---

## Key Technologies

- **Jekyll** 4.x (Ruby-based static site generator)
- **Theme:** TBD (modern, mobile-responsive, SEO-friendly)
- **SEO:** jekyll-seo-tag plugin
- **Sitemap:** jekyll-sitemap plugin
- **Minimal JavaScript:** Prefer CSS-only solutions where possible
- **Contact Form:** Formspree or similar (static site compatible)
- **Image Optimization:** Use Jekyll picture tag or responsive images

---

## Content Translation Strategy

### Phase 1 (Current): Polish Only
- Scrape and structure all Polish content
- Build complete PL site first

### Phase 2 (Future - ROADMAP): Multilingual
- Use OpenRouter AI models (Kimi 2.5 or similar cost-effective option) to translate:
  - PL → EN (English)
  - PL → DE (German)
- Use Jekyll i18n plugin (`jekyll-multiple-languages-plugin` or similar)
- Create `_i18n/` directory structure:
  ```
  _i18n/
  ├── pl/
  ├── en/
  └── de/
  ```

**Translation Glossary:** Keep specialized landscape architecture terms in `memory/translation-glossary.md`

---

## Content Scraping & Structuring Workflow

1. **Scrape Phase** (DONE): Downloaded site structure to `analysis/site-scrape.md`
2. **Asset Download Phase**: Download all images, PDFs, and media to `scraped-content/`
3. **Content Structuring Phase**: Use AI (OpenRouter) to convert scraped HTML to structured YAML/JSON
4. **Jekyll Integration Phase**: Convert structured data to Jekyll markdown files with frontmatter

---

## SEO Requirements

### Must-Have SEO Elements

1. **Meta Tags:**
   - Title tags (unique per page, max 60 chars)
   - Meta descriptions (unique per page, 150-160 chars)
   - Open Graph tags (og:title, og:description, og:image)
   - Twitter Card tags

2. **Structured Data:**
   - LocalBusiness schema (JSON-LD)
   - Service schema for each service offering
   - BreadcrumbList schema

3. **Performance:**
   - Optimized images (WebP with fallbacks)
   - Lazy loading for images
   - Minified CSS/JS
   - Fast page load times

4. **Sitemap & Robots:**
   - XML sitemap (jekyll-sitemap)
   - robots.txt
   - 301 redirects for old URLs (via Netlify _redirects or similar)

5. **Mobile-First:**
   - Responsive design
   - Touch-friendly navigation
   - Fast mobile load times

---

## Git Workflow

### Commit Message Convention

Use conventional commits format:
```
type(scope): description

Types: feat, fix, docs, style, refactor, content, design
Examples:
  feat(structure): add Jekyll scaffolding
  content(oferta): add dendrology services pages
  design(theme): customize header and navigation
  docs(memory): record content mapping decisions
```

### Branch Strategy (Optional, for complex work)

- `main` — production-ready, deployed to GitHub Pages
- `dev` — integration branch for testing
- Feature branches: `feature/portfolio-grid`, `content/services`, etc.

For this project, working directly on `main` is fine since it's private and demo-only.

---

## Commands & Scripts

### Jekyll Development

```bash
cd /home/luna/ikropka-migration/site
bundle install              # Install Jekyll and dependencies
bundle exec jekyll serve    # Run local dev server (http://localhost:4000)
bundle exec jekyll build    # Build static site to _site/
```

### Content Translation (Future)

```bash
# When implementing multilingual support:
cd /home/luna/ikropka-migration
./scripts/translate-content.sh pl en  # Translate PL → EN using OpenRouter
```

---

## Before Starting Any Work

1. **Read `MEMORY.md`** to understand current decisions and context
2. **Check `ROADMAP.md`** to see what's planned vs what's done
3. **Review `analysis/site-scrape.md`** to understand source content
4. **Update `MEMORY.md`** after making any significant decisions

---

## Notes for Claude

- **Separation of Concerns:** This project's memory is SEPARATE from homelab infra notes
- **Cost-Conscious AI Usage:** Use cost-effective models (Kimi 2.5 ~$0.375/1M input tokens) for bulk translation
- **SEO Priority:** Every page needs proper meta tags, structured data, and mobile optimization
- **Content Accuracy:** Landscape architecture is a specialized field — preserve technical terminology accuracy
- **Demo Status:** This is a preview build. Final hosting TBD. Don't over-engineer for GitHub Pages limitations.

---

## Questions? Need Guidance?

If you're unsure about:
- **Content structure decisions** → Use `/grill-me` skill to interview the user
- **Technical implementation** → Check Jekyll docs, existing theme documentation
- **SEO best practices** → Refer to this file's SEO requirements section
- **Memory/documentation** → Record decisions in `MEMORY.md`, update `ROADMAP.md`

---

**Last Updated:** 2026-07-16
**Status:** Project setup phase

---

## CRITICAL: Task Execution Policy (Inherited from Home CLAUDE.md)

**NEVER defer or postpone planned work without explicit user approval.**

When working on this project:
- ✅ Execute milestones fully as specified in PHASE1-EXECUTION-PLAN.md
- ✅ Ask for clarification if requirements unclear
- ✅ Ask for approval before changing scope
- ❌ NO silent deferrals with "TBD" notes
- ❌ NO placeholders that won't be revisited
- ❌ NO skipping tasks without explicit permission

**If blocked:** Communicate clearly → Propose alternatives → Wait for approval → Document in MEMORY.md

See `/home/luna/CLAUDE.md` for full policy details.

