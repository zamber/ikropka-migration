# Test Pages for Content Extraction Refinement

These 5 diverse pages will be used to refine the AI extraction prompt and YAML schema.

## 1. Homepage (Complex)
**URL:** https://ikropka.eu/
**Type:** Homepage
**Complexity:** High
**Features:**
- Hero image carousel/slider
- Three-pillar business model section (Design, Dendrology, Supervision)
- "Our Assets" section (6 key strengths as tiles)
- Featured projects gallery (3 recent projects)
- Client testimonials/references (2013-2019)
- Contact form (placeholder for Phase 2)
- Statistics section

**Why selected:** Most complex page type with diverse content sections and components.

---

## 2. About Page (Static)
**URL:** https://ikropka.eu/o-nas/
**Type:** Static page
**Complexity:** Medium
**Features:**
- Company overview and mission
- Founder credentials (Dominika Krop-Andrzejczuk)
- Three operational pillars section
- Expertise & approach description
- Credentials gallery (certificate images)
- Statistics section (4 metrics: clients, projects, supervision, trees)
- Partnerships list

**Why selected:** Representative of structured static content with mixed text/image sections.

---

## 3. Service Detail Page (Structured)
**URL:** https://ikropka.eu/oferta/inwentaryzacje-dendrologiczne/
**Type:** Service page
**Complexity:** Medium
**Features:**
- Hero section with service introduction
- Service description (comprehensive explanation)
- Service components (2-part structure: descriptive + graphic)
- Additional offerings list
- Project portfolio carousel (case studies)
- Client references/testimonials
- Contact section

**Why selected:** Represents the 14 service subpages with consistent structure.

---

## 4. Portfolio Project Page (Gallery-focused)
**URL:** https://ikropka.eu/projekt/rewaloryzacja-zabytkowej-alei-projekt-poprawy-warunkow-siedliskowych-przy-al-paderewskiego/
**Type:** Portfolio single project
**Complexity:** Medium
**Features:**
- Project metadata (client, location, year, scope, area)
- Image gallery (multiple project photos)
- Project description sections
- Challenges & solutions sections
- Tags/categories

**Why selected:** Represents 130+ portfolio projects with image galleries and structured metadata.

---

## 5. News/Blog Post (Article)
**URL:** https://ikropka.eu/posiadamy-nowe-uprawnienia-branzowe-ett-european-tree-technician-ekspert-arborysta-dendrolog/
**Type:** Blog post / News article
**Complexity:** Low
**Features:**
- Title and date
- Article content (multi-paragraph text)
- Featured image
- Optional embedded media
- Categories/tags

**Why selected:** Represents blog/news content type with simpler structure.

---

## Success Criteria

For each test page, the extraction must achieve:
- ✅ Valid YAML syntax (no errors)
- ✅ All important content captured (no loss)
- ✅ Proper structure matching Jekyll expectations
- ✅ No manual editing required
- ✅ Images properly extracted with paths/alt text
- ✅ Metadata fields complete

## Refinement Process

1. Run extraction on page
2. Manually review YAML output
3. Identify issues (missing fields, incorrect structure, malformed YAML)
4. Refine prompt and/or schema
5. Re-run extraction
6. Repeat until clean (zero manual fixes)

---

**Note:** Only proceed to Milestone 5 (batch processing ~145 pages) after all 5 test pages extract cleanly.
