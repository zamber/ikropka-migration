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
