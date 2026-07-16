# IKROPKA Migration - Next Steps

**Last Updated:** 2026-07-16  
**Current Status:** Milestone 5 Complete ✅

---

## ✅ Completed Milestones

### Milestone 1: Project Setup & Planning
- GitHub repository created (private)
- Directory structure established
- Site analysis completed (150+ pages, 600+ images)
- Technology stack decided (Jekyll + Minimal Mistakes)
- Roadmap created with 10 milestones

### Milestone 2: Jekyll Scaffolding
- Jekyll 4.4.1 installed
- Minimal Mistakes 4.28.0 theme configured
- Collections set up (_portfolio, _services)
- Navigation structure created
- Placeholder pages added

### Milestone 3: Image Migration & Optimization
- Downloaded 364 images via WordPress REST API (88MB)
- Deduplicated to 349 unique images
- Optimized to 696 files (WebP + JPEG fallback, 101MB)
- Zero errors during processing

### Milestone 4: Content Extraction with AI
- Selected Kimi K2.7 Code model (OpenRouter API)
- Created extraction scripts and YAML schemas
- Tested on 5 diverse pages (validation loop)
- Batch extracted 157 YAML files (63 minutes)
- Performance analysis completed

### Milestone 5: Jekyll Content Integration
- Created conversion script (YAML → Jekyll markdown)
- Converted 152 files (3 pages, 13 services, 72 portfolio, 64 posts)
- Organized in Jekyll collections
- Polish content preserved perfectly
- All files ready for Jekyll processing

---

## 🚧 Current Milestone: 6 - Portfolio Features

**Goal:** Add lazy loading, fuzzy search, and category filtering for 72 portfolio projects

### Tasks Remaining

1. **Create portfolio index page** (`site/_pages/portfolio.md`)
   - List all 72 projects
   - Add category filter buttons (Projekty, Zabytkowe, Szkolenia)
   - Implement fuzzy search with fuse.js

2. **Create category pages**
   - `/portfolio/projekty/` - Regular projects
   - `/portfolio/zabytkowe/` - Historic monument projects  
   - `/portfolio/szkolenia/` - Training/education projects

3. **Add lazy loading for images**
   - Use Intersection Observer API
   - Or `loading="lazy"` attribute (simpler)

4. **Create portfolio layout template**
   - `site/_layouts/portfolio_single.html`
   - Include gallery support
   - Project metadata display

5. **Test portfolio rendering**
   - Verify all 72 projects display correctly
   - Test category filtering
   - Test search functionality

---

## 📋 Upcoming Milestones

### Milestone 7: SEO Optimization
- Meta tags for all pages
- Open Graph tags
- XML sitemap
- robots.txt
- Schema.org markup for portfolio/services

### Milestone 8: Design Customization
- Extract IKROPKA branding (colors, fonts, logo)
- Customize Minimal Mistakes theme
- Mobile responsiveness testing
- Polish language UI strings

### Milestone 9: Final QA
- Content review (spot-check 10-20 pages)
- Link checking
- Image loading verification
- Cross-browser testing
- Performance audit

### Milestone 10: GitHub Pages Deployment
- Build Jekyll site
- Configure GitHub Pages
- Set up baseurl correctly
- Test live site
- Document deployment process

---

## 🔧 Technical Debt

### Jekyll Build Issues (Low Priority)
- Local gem environment has path conflicts
- Build works with direct gem binary: `~/.gem/gems/jekyll-4.4.1/exe/jekyll build`
- **Fix:** Set up clean Ruby environment or use Docker
- **Workaround:** GitHub Pages will build automatically on push

### Missing Features (Will Add in Milestone 6+)
- Portfolio grid include on homepage
- Custom layouts for portfolio single pages
- Custom layouts for service pages
- Contact form integration (deferred to Phase 2)

### Performance Optimizations (Future)
- Consider CDN for images (if repo size becomes issue)
- Implement service worker for offline support
- Add asset preloading for critical resources

---

## 📊 Project Statistics

| Metric | Count | Status |
|--------|-------|--------|
| **Pages** | 3 | ✅ Converted |
| **Services** | 13 | ✅ Converted |
| **Portfolio Projects** | 72 | ✅ Converted |
| **Blog Posts** | 64 | ✅ Converted |
| **Images** | 696 | ✅ Optimized |
| **Total Content Files** | 152 | ✅ Ready |

**Estimated Progress:** ~50% complete (5 of 10 milestones done)

---

## 🎯 Immediate Next Actions

1. **Continue with Milestone 6** - Portfolio features implementation
2. **Fix Jekyll build** - Set up clean environment or use GitHub Pages build
3. **Create layouts** - Portfolio single, service single, custom homepage sections
4. **Test rendering** - Verify all content displays correctly

---

## 📝 Notes

- OpenRouter API key stored in `~/.openclaw/workspace/.env_luna` (low budget, safe if leaked)
- All Polish content preserved perfectly through extraction/conversion pipeline
- Image optimization strategy: WebP primary + JPEG fallback for compatibility
- Performance bottleneck identified: Kimi K2.7 Code slow (~2-4 min per API call)
- For future migrations: Use GPT-4o-mini or Gemini Flash for 10-20× speedup

