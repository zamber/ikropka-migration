# IKROPKA Migration Project - ROADMAP

**Project:** ikropka.eu website migration to Jekyll
**Owner:** Piotr Zaborowski (zamber88@gmail.com)
**Last Updated:** 2026-07-16

---

## Current Status: Phase 1 — Setup & Planning

---

## Phase 1: Foundation & Polish Site (CURRENT)

**Goal:** Build complete, SEO-optimized Polish-language Jekyll site

### 1.1 Project Setup ✓ (In Progress)
- [x] Create project directory structure
- [x] Write CLAUDE.md (project guidance)
- [x] Write ROADMAP.md (this file)
- [ ] Create GitHub private repository
- [ ] Initialize MEMORY.md
- [ ] Set up Git workflow

### 1.2 Content Scraping & Analysis
- [x] Scrape site structure (site-scrape.md exists)
- [ ] Download all images and media assets
- [ ] Download all portfolio project pages
- [ ] Catalog all content types (services, projects, blog posts, etc.)
- [ ] Create URL mapping (old → new structure)

### 1.3 Jekyll Scaffolding
- [ ] Choose Jekyll theme (modern, mobile-responsive, SEO-friendly)
- [ ] Set up Jekyll project structure
- [ ] Configure _config.yml
- [ ] Install required plugins (SEO, sitemap, etc.)
- [ ] Test local development environment

### 1.4 Content Structuring with AI
- [ ] Select OpenRouter model (Kimi 2.5 or cost-effective alternative)
- [ ] Create content extraction prompts
- [ ] Convert scraped HTML → structured YAML/JSON
- [ ] Validate structured data quality
- [ ] Store in `content-structured/` directory

### 1.5 Jekyll Content Integration
- [ ] Convert structured data → Jekyll markdown + frontmatter
- [ ] Populate service pages (14 offer subpages)
- [ ] Populate portfolio projects (130+ projects)
- [ ] Create homepage
- [ ] Create about page (O nas)
- [ ] Create contact page with form
- [ ] Blog/news posts migration

### 1.6 Design & SEO Optimization
- [ ] Customize theme (colors, fonts, branding)
- [ ] Implement hero slider (homepage)
- [ ] Add testimonials carousel
- [ ] Optimize images (WebP, lazy loading)
- [ ] Add meta tags to all pages
- [ ] Implement structured data (JSON-LD)
- [ ] Create XML sitemap
- [ ] Create robots.txt
- [ ] Test mobile responsiveness
- [ ] Performance audit (Lighthouse)

### 1.7 Forms & Interactive Elements
- [ ] Implement contact form (Formspree or alternative)
- [ ] Add GDPR consent checkboxes
- [ ] File upload capability (if possible with static site)
- [ ] Google Maps integration (contact page)

### 1.8 GitHub Pages Deployment
- [ ] Push to GitHub repository
- [ ] Configure GitHub Pages
- [ ] Test deployment
- [ ] Share preview URL with stakeholders

**Phase 1 Target Completion:** TBD

---

## Phase 2: Multilingual Support (FUTURE)

**Goal:** Add English and German language versions

### 2.1 Translation Infrastructure
- [ ] Install Jekyll i18n plugin (`jekyll-multiple-languages-plugin` or similar)
- [ ] Set up `_i18n/` directory structure (pl/, en/, de/)
- [ ] Create language switcher UI component
- [ ] Update navigation for language switching

### 2.2 AI-Powered Translation
- [ ] Create translation glossary (specialized landscape architecture terms)
- [ ] Set up OpenRouter translation pipeline
- [ ] Translate PL → EN (all content)
- [ ] Translate PL → DE (all content)
- [ ] Review and validate translations (human QA)
- [ ] Adjust for cultural/regional differences

### 2.3 Multilingual SEO
- [ ] Add hreflang tags
- [ ] Create language-specific sitemaps
- [ ] Localize meta descriptions
- [ ] Update structured data for each language

### 2.4 Testing & Launch
- [ ] Test language switching
- [ ] Verify all links work in all languages
- [ ] SEO audit for each language
- [ ] Deploy multilingual site

**Phase 2 Target Start:** After Phase 1 complete and stable

---

## Phase 3: Production Deployment (FUTURE)

**Goal:** Move from GitHub Pages demo to commercial hosting

**Note:** GitHub Pages TOS prohibits commercial use. This is demo-only.

### 3.1 Hosting Selection
- [ ] Choose production hosting provider (Netlify, Vercel, VPS, etc.)
- [ ] Evaluate CDN options
- [ ] Plan for custom domain (ikropka.eu or similar)

### 3.2 Migration
- [ ] Set up production hosting environment
- [ ] Configure CI/CD pipeline
- [ ] Set up 301 redirects from old URLs
- [ ] DNS configuration
- [ ] SSL certificate setup

### 3.3 Launch
- [ ] Final SEO audit
- [ ] Final performance audit
- [ ] Backup old WordPress site
- [ ] Switch DNS to new site
- [ ] Monitor traffic and errors
- [ ] Submit new sitemap to Google Search Console

**Phase 3 Target Start:** TBD

---

## Phase 4: Enhancements (FUTURE)

**Goal:** Add advanced features and optimizations

### Potential Enhancements
- [ ] Blog/news section with RSS feed
- [ ] Portfolio filtering by category/tags
- [ ] Search functionality (Algolia, Lunr.js, or similar)
- [ ] Enhanced image galleries (lightbox, etc.)
- [ ] Client portal / login area (if needed)
- [ ] Integration with CRM/project management tools
- [ ] A/B testing for conversion optimization
- [ ] Analytics setup (privacy-friendly, GDPR-compliant)
- [ ] Newsletter signup integration
- [ ] Social media feed integration

**Phase 4:** Ongoing enhancements based on user feedback and analytics

---

## Open Questions & Decisions Needed

### Theme Selection
**Question:** Which Jekyll theme should we use?
**Options:**
- Minimal Mistakes (highly customizable, SEO-focused)
- Beautiful Jekyll (simple, modern)
- Jekyll Business (business-focused)
- Custom theme from scratch

**Decision:** TBD — User approval needed

### Contact Form Solution
**Question:** How to handle contact forms on static site?
**Options:**
- Formspree (free tier: 50 submissions/month)
- Netlify Forms (if hosting on Netlify)
- FormKeep
- Custom backend API

**Decision:** TBD

### Portfolio Organization
**Question:** How to organize 130+ portfolio projects?
**Options:**
- Paginated grid (20-30 per page)
- Category-based filtering (Historic, Projects, Training)
- Infinite scroll
- Combination of filtering + pagination

**Decision:** TBD

### Image Hosting
**Question:** Where to host images?
**Options:**
- GitHub repo (increases repo size, but simplest)
- External CDN (Cloudinary, Imgix, etc.)
- Netlify Large Media (if using Netlify)

**Decision:** TBD — Start with GitHub repo, evaluate later

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Jekyll learning curve | Medium | Use well-documented theme, follow tutorials |
| Content translation quality | High | Human review after AI translation, use glossary |
| Image size / repo bloat | Medium | Optimize images, consider external CDN later |
| Contact form limitations | Low | Use established third-party service (Formspree) |
| SEO loss during migration | High | 301 redirects, preserve URLs where possible, submit new sitemap |
| GitHub Pages commercial use TOS | Medium | Clearly mark as demo, plan Phase 3 migration to commercial hosting |

---

## Success Metrics (Phase 1)

- [ ] All 150+ pages migrated successfully
- [ ] Mobile-responsive design (passes Google Mobile-Friendly Test)
- [ ] Lighthouse score: 90+ Performance, 100 Accessibility, 100 Best Practices, 100 SEO
- [ ] All images optimized (< 500KB each)
- [ ] Page load time < 3 seconds (3G connection)
- [ ] Zero broken links
- [ ] Contact form functional
- [ ] Client/stakeholder approval

---

**Next Steps:**
1. Get user approval on Phase 1 plan
2. Select Jekyll theme
3. Download all site assets
4. Begin content structuring with AI
