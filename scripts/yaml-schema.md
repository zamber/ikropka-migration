# YAML Schema for IKROPKA Content Extraction

This document defines the YAML structure for different page types in the Jekyll migration.

---

## 1. Homepage Schema

```yaml
---
layout: home
title: "IKROPKA — Pracownia Architektury Krajobrazu"
description: "Brief meta description for SEO (150-160 chars)"
permalink: /

# Hero Slider Section
hero:
  slides:
    - image: /assets/images/hero-1.jpg
      alt: "Image description"
      caption: "Optional caption text"
      cta_text: "Call to action button text"
      cta_url: "/oferta/"
    - image: /assets/images/hero-2.jpg
      alt: "Image description"

# Content Sections (ordered array)
sections:
  - type: intro
    heading: "Company tagline or intro heading"
    content: |
      Multi-line intro text.
      Can span multiple paragraphs.

  - type: three_pillars
    heading: "Nasze usługi" # or similar
    items:
      - icon: "design" # icon identifier
        title: "Projekty"
        description: "Design projects adapted to client specifications"
        link: "/oferta/#projekty"
      - icon: "tree"
        title: "Dendrologia"
        description: "Tree inventories and expert assessments"
        link: "/oferta/#dendrologia"
      - icon: "supervision"
        title: "Nadzory"
        description: "Supervision during investment processes"
        link: "/oferta/#nadzory"

  - type: strengths
    heading: "Nasze atuty"
    items:
      - icon: "experience" # icon identifier
        title: "Doświadczenie"
        description: "Short description"
      - icon: "quality"
        title: "Jakość"
        description: "Short description"
      # ... up to 6 items

  - type: stats
    heading: "Nasze osiągnięcia w liczbach"
    items:
      - number: "1110"
        label: "Zadowolonych klientów"
      - number: "352"
        label: "Zrealizowanych projektów"
      - number: "125"
        label: "Nadzorów"
      - number: "110350"
        label: "Zinwentaryzowanych drzew"

  - type: featured_projects
    heading: "Wybrane projekty"
    items:
      - slug: "projekt-slug-1" # references _portfolio/projekt-slug-1.md
        title: "Project title (if needed)"
        thumbnail: "/assets/images/projects/thumb1.jpg"
      - slug: "projekt-slug-2"

  - type: testimonials
    heading: "Referencje"
    items:
      - author: "Jan Kowalski"
        organization: "Gmina Wrocław"
        year: "2019"
        content: "Testimonial quote text..."
      - author: "Anna Nowak"
        organization: "Firma ABC Sp. z o.o."
        year: "2018"
        content: "Testimonial quote..."

  - type: contact_cta
    heading: "Skontaktuj się z nami"
    text: "Brief intro text for contact section"
    note: "Contact form deferred to Phase 2/3"
---
```

---

## 2. About Page Schema

```yaml
---
layout: page
title: "O nas"
description: "About IKROPKA landscape architecture studio"
permalink: /o-nas/

sections:
  - type: intro
    heading: "Pracujemy dynamicznie, działamy aktywnie"
    content: |
      Multi-paragraph company overview.
      Mission statement and history.

  - type: founder
    heading: "Kierownik pracowni"
    name: "Dominika Krop-Andrzejczuk"
    credentials:
      - "Architekt krajobrazu"
      - "Inspektor nadzoru zieleni"
      - "Other qualifications..."
    bio: |
      Detailed bio text about the founder.

  - type: three_pillars
    heading: "Zakres działalności"
    items:
      - title: "Projekty"
        description: "..."
      - title: "Dendrologia"
        description: "..."
      - title: "Nadzory"
        description: "..."

  - type: expertise
    heading: "Nasza filozofia"
    content: |
      Text about approach, collaboration, quality standards.

  - type: credentials_gallery
    heading: "Kwalifikacje i szkolenia"
    images:
      - image: /assets/images/credentials/cert1.jpg
        alt: "Certificate description"
        caption: "Optional caption"
      - image: /assets/images/credentials/cert2.jpg
        alt: "Certificate description"

  - type: stats
    heading: "Nasze osiągnięcia"
    items:
      - number: "1110"
        label: "Klientów"
      - number: "352"
        label: "Projektów"
      - number: "125"
        label: "Nadzorów"
      - number: "110350"
        label: "Drzew"

  - type: partnerships
    heading: "Współpraca"
    content: |
      Text about partner organizations.
    logos:
      - image: /assets/images/partners/logo1.jpg
        alt: "Partner name"
      - image: /assets/images/partners/logo2.jpg
        alt: "Partner name"
---
```

---

## 3. Service Page Schema

```yaml
---
layout: service
title: "Inwentaryzacje Dendrologiczne"
description: "Professional tree inventory services in Wrocław"
permalink: /oferta/inwentaryzacje-dendrologiczne/

category: services
service_type: dendrology # or: design, supervision, consulting, training

hero_image: /assets/images/services/inwentaryzacje-hero.jpg
hero_alt: "Tree inventory field work"

sections:
  - type: intro
    content: |
      Service introduction paragraph.
      Key benefits and overview.

  - type: description
    heading: "Czym jest inwentaryzacja dendrologiczna?"
    content: |
      Detailed service description.
      Can span multiple paragraphs.

  - type: components
    heading: "Co obejmuje inwentaryzacja"
    items:
      - title: "Część opisowa"
        description: "Lista drzew z nazwami łacińskimi, parametry dendrometryczne, stan sanitarny..."
      - title: "Część graficzna"
        description: "Lokalizacja drzew w AutoCAD lub GIS z numerami ewidencyjnymi..."

  - type: features
    heading: "Co oferujemy"
    items:
      - "Feature 1: Detailed species identification"
      - "Feature 2: Health assessments"
      - "Feature 3: AutoCAD/GIS documentation"
      - "Feature 4: Photographic documentation"

  - type: process
    heading: "Proces realizacji"
    steps:
      - number: 1
        title: "Wizja lokalna"
        description: "Initial site visit and assessment"
      - number: 2
        title: "Inwentaryzacja"
        description: "Field survey and measurements"
      - number: 3
        title: "Dokumentacja"
        description: "Report preparation"
      - number: 4
        title: "Doradztwo"
        description: "Post-project consultation"

  - type: projects_carousel
    heading: "Wybrane realizacje"
    note: "Reference to related portfolio projects"
    projects:
      - slug: "projekt-slug-1"
      - slug: "projekt-slug-2"

  - type: testimonials
    heading: "Referencje klientów"
    items:
      - author: "Client name"
        organization: "Organization"
        year: "2020"
        content: "Testimonial text..."

  - type: cta
    heading: "Potrzebujesz inwentaryzacji?"
    text: "Contact us for a quote"
    button_text: "Kontakt"
    button_url: "/kontakt/"

# Related services (sidebar)
related_services:
  - slug: "operat-dendrologiczny"
    title: "Operat dendrologiczny"
  - slug: "dendrolog-opinie-ekspertyzy"
    title: "Dendrolog - opinie i ekspertyzy"
---
```

---

## 4. Portfolio Project Schema

```yaml
---
layout: portfolio_single
title: "Rewaloryzacja zabytkowej alei przy al. Paderewskiego"
description: "Project description for SEO (1-2 sentences)"
permalink: /portfolio/rewaloryzacja-alei-paderewskiego/

category: projekty # Options: projekty, zabytkowe, szkolenia
featured_image: /assets/images/portfolio/paderewskiego/main.jpg

# Project metadata
project_meta:
  client: "Gmina Wrocław"
  location: "Wrocław, woj. dolnośląskie"
  year: "2025"
  scope: "Projekt poprawy warunków siedliskowych" # or: Projekt zagospodarowania, Inwentaryzacja, etc.
  area: "2.5 ha" # optional
  status: "W realizacji" # or: Zrealizowany, Koncepcja

# Image gallery
gallery:
  - image: /assets/images/portfolio/paderewskiego/photo1.jpg
    alt: "Description of image"
    caption: "Optional caption text"
  - image: /assets/images/portfolio/paderewskiego/photo2.jpg
    alt: "Description"
  - image: /assets/images/portfolio/paderewskiego/photo3.jpg
    alt: "Description"

# Project content sections
sections:
  - type: intro
    content: |
      Opening paragraph describing the project context.

  - type: description
    heading: "Opis projektu"
    content: |
      Multi-paragraph detailed description.
      Project goals, context, significance.

  - type: challenges
    heading: "Wyzwania"
    content: |
      Challenges faced in the project.
      Technical, environmental, or regulatory issues.

  - type: solution
    heading: "Rozwiązania projektowe"
    content: |
      Solutions implemented.
      Design decisions and innovations.

  - type: results
    heading: "Efekty"
    content: |
      Project outcomes and benefits.
      Impact on the environment and community.

# Optional: Embedded documents (PDFs, plans)
documents:
  - title: "Plan zagospodarowania"
    file: /assets/documents/paderewskiego-plan.pdf
  - title: "Inwentaryzacja"
    file: /assets/documents/paderewskiego-inwentaryzacja.pdf

# Tags for filtering
tags:
  - aleja
  - drzewa zabytkowe
  - rewaloryzacja
  - Wrocław
---
```

---

## 5. Blog/News Post Schema

```yaml
---
layout: post
title: "Posiadamy nowe uprawnienia branżowe – ETT European Tree Technician"
description: "Team member achieved European Tree Technician certification"
date: 2025-10-15 # YYYY-MM-DD format
author: "IKROPKA"
permalink: /aktualnosci/uprawnienia-ett-european-tree-technician/

categories:
  - aktualności
  - szkolenia
  - dendrologia

tags:
  - ETT
  - certyfikat
  - uprawnienia
  - arborysta

featured_image: /assets/images/news/ett-certificate.jpg
featured_image_alt: "ETT European Tree Technician certificate"

# Post content
sections:
  - type: intro
    content: |
      Opening paragraph with key announcement.

  - type: body
    content: |
      Main article text.
      Can span multiple paragraphs with full details.

      Second paragraph...

  - type: quote
    text: "Notable quote from the article"
    author: "Optional attribution"

  - type: image
    image: /assets/images/news/ett-training.jpg
    alt: "Training session photo"
    caption: "Optional caption"

  - type: conclusion
    content: |
      Closing paragraph.

# Optional: Related projects or services
related:
  - type: service
    slug: "dendrolog-opinie-ekspertyzy"
  - type: project
    slug: "projekt-slug"
---
```

---

## General YAML Guidelines

### Frontmatter Fields (Common to All)
- `layout`: Jekyll layout name (home, page, service, portfolio_single, post)
- `title`: Page title (plain text, will be escaped)
- `description`: SEO meta description (150-160 chars recommended)
- `permalink`: URL path (must start with `/` and end with `/` for directories)

### Content Sections
- Use ordered array: `sections: []`
- Each section has a `type` field identifying its structure
- Use `|` for multi-line YAML strings (preserves line breaks)
- Use `>` for folded multi-line strings (joins lines into paragraph)

### Images
- All image paths start with `/assets/images/`
- Always include `alt` text (accessibility)
- `caption` is optional

### Lists
- Use YAML array syntax: `items: []` or `- item`
- Keep structure consistent within each type

### Validation
- Ensure proper indentation (2 spaces per level)
- Quote strings with special characters: `title: "Text: with punctuation"`
- Use `|` for multi-paragraph text blocks
- No tabs (use spaces only)

---

## Edge Cases

### Unrecognized HTML Elements
```yaml
- type: html_block
  content: |
    <div class="custom-widget">
      Raw HTML preserved here
    </div>
```

### Embedded Media (Videos, iframes)
```yaml
- type: embed
  embed_type: youtube # or: vimeo, iframe
  url: "https://youtube.com/watch?v=..."
  title: "Video title"
```

### WordPress Shortcodes
```yaml
- type: shortcode
  shortcode_name: "gallery"
  attributes:
    ids: "1,2,3"
    columns: "3"
  note: "WordPress shortcode - may need manual conversion"
```

### Forms (Deferred)
```yaml
- type: contact_form
  note: "Contact Form 7 detected - deferred to Phase 2/3"
  original_shortcode: "[contact-form-7 id='123']"
```

---

**Version:** 1.0
**Last Updated:** 2026-07-16
**Status:** Draft for refinement loop
