# Content Extraction Prompt Template

This prompt template is used with Kimi K2.5 (via OpenRouter) to extract structured YAML from WordPress HTML pages.

---

## System Prompt (Consistent for all pages)

```
You are an expert at extracting structured content from HTML and converting it to clean, valid YAML for Jekyll static sites.

Your task is to analyze WordPress HTML pages and output ONLY valid YAML frontmatter + content following the provided schema.

CRITICAL RULES:
1. Output ONLY valid YAML - no explanations, no markdown code blocks, no preamble
2. Preserve all important content - no data loss
3. Extract semantic meaning, not just raw HTML
4. Follow the exact schema structure provided
5. Use multi-line YAML strings (|) for paragraphs and long text
6. Ensure proper indentation (2 spaces per level)
7. Quote strings with special characters
8. Extract image paths, alt text, and captions
9. Identify section types correctly (intro, description, gallery, etc.)
10. If unsure about a section type, use "content" or "html_block"
```

---

## Page-Type-Specific Prompts

### Homepage Extraction Prompt

```markdown
TASK: Extract content from the IKROPKA homepage into YAML format.

PAGE TYPE: Homepage
LAYOUT: home

SCHEMA TO FOLLOW:
---
layout: home
title: "IKROPKA — Pracownia Architektury Krajobrazu"
description: "SEO description (150-160 chars)"
permalink: /

hero:
  slides:
    - image: /assets/images/filename.jpg
      alt: "Alt text"
      caption: "Optional caption"

sections:
  - type: intro
    heading: "Heading text"
    content: |
      Multi-line content...

  - type: three_pillars
    heading: "Section heading"
    items:
      - icon: "icon_name"
        title: "Title"
        description: "Description text"
        link: "/url/"

  - type: strengths
    heading: "Nasze atuty"
    items:
      - icon: "icon_name"
        title: "Title"
        description: "Description"

  - type: stats
    heading: "Statistics heading"
    items:
      - number: "1110"
        label: "Label text"

  - type: featured_projects
    heading: "Wybrane projekty"
    items:
      - slug: "project-slug"
        title: "Project title"
        thumbnail: "/assets/images/thumb.jpg"

  - type: testimonials
    heading: "Referencje"
    items:
      - author: "Name"
        organization: "Organization"
        year: "2019"
        content: "Quote text..."

  - type: contact_cta
    heading: "Contact heading"
    text: "Contact intro text"
    note: "Contact form deferred to Phase 2/3"
---

EXTRACTION INSTRUCTIONS:
1. Extract the site title and create a brief SEO description
2. Identify hero slider images (look for carousel/slider sections) - extract image paths, alt text, captions
3. Parse content sections in order:
   - Intro/welcome section
   - Three pillars (Design, Dendrology, Supervision) - extract icons, titles, descriptions
   - "Our strengths" tiles - extract up to 6 items
   - Statistics section - extract 4 metrics (clients, projects, supervision, trees)
   - Featured projects - extract 3 recent project slugs/titles/thumbnails
   - Testimonials - extract client quotes with attribution
   - Contact CTA section
4. For each section, identify the type and extract structured data
5. Convert all image URLs to relative paths starting with /assets/images/
6. Preserve Polish language text exactly as-is

HTML INPUT:
{HTML_CONTENT_HERE}

OUTPUT (YAML ONLY):
```

### Service Page Extraction Prompt

```markdown
TASK: Extract content from an IKROPKA service page into YAML format.

PAGE TYPE: Service detail page
LAYOUT: service

SCHEMA TO FOLLOW:
---
layout: service
title: "Service name"
description: "Service description for SEO"
permalink: /oferta/service-slug/

category: services
service_type: dendrology # or: design, supervision, consulting, training

hero_image: /assets/images/services/hero.jpg
hero_alt: "Hero image description"

sections:
  - type: intro
    content: |
      Introduction paragraph

  - type: description
    heading: "Heading"
    content: |
      Detailed description

  - type: components
    heading: "What it includes"
    items:
      - title: "Component name"
        description: "Component description"

  - type: features
    heading: "What we offer"
    items:
      - "Feature 1"
      - "Feature 2"

  - type: process
    heading: "Process"
    steps:
      - number: 1
        title: "Step title"
        description: "Step description"

  - type: projects_carousel
    heading: "Selected projects"
    note: "Reference to portfolio projects"
    projects:
      - slug: "project-slug"

  - type: testimonials
    heading: "Client references"
    items:
      - author: "Name"
        organization: "Organization"
        year: "2020"
        content: "Quote"

  - type: cta
    heading: "Call to action"
    text: "CTA text"
    button_text: "Button text"
    button_url: "/kontakt/"

related_services:
  - slug: "related-service-1"
    title: "Service title"
---

EXTRACTION INSTRUCTIONS:
1. Extract service title and create SEO description
2. Generate permalink from title (lowercase, hyphens, Polish characters preserved)
3. Identify service type (dendrology, design, supervision, consulting, training)
4. Extract hero image if present
5. Parse content sections in order:
   - Intro paragraph
   - Service description
   - Components/what's included
   - Features list
   - Process steps (if present)
   - Related projects carousel
   - Client testimonials
   - Call to action
6. Extract related services from sidebar or footer
7. Convert image URLs to relative paths
8. Preserve Polish text exactly

HTML INPUT:
{HTML_CONTENT_HERE}

OUTPUT (YAML ONLY):
```

### Portfolio Project Extraction Prompt

```markdown
TASK: Extract content from an IKROPKA portfolio project page into YAML format.

PAGE TYPE: Portfolio project single
LAYOUT: portfolio_single

SCHEMA TO FOLLOW:
---
layout: portfolio_single
title: "Project title"
description: "Project description (1-2 sentences)"
permalink: /portfolio/project-slug/

category: projekty # Options: projekty, zabytkowe, szkolenia
featured_image: /assets/images/portfolio/project/main.jpg

project_meta:
  client: "Client name"
  location: "City, województwo"
  year: "2025"
  scope: "Project type/scope"
  area: "X ha" # optional
  status: "Status" # W realizacji, Zrealizowany, Koncepcja

gallery:
  - image: /assets/images/portfolio/project/photo1.jpg
    alt: "Image description"
    caption: "Optional caption"

sections:
  - type: intro
    content: |
      Opening paragraph

  - type: description
    heading: "Project description"
    content: |
      Detailed description

  - type: challenges
    heading: "Challenges"
    content: |
      Challenges text

  - type: solution
    heading: "Solutions"
    content: |
      Solutions text

  - type: results
    heading: "Results"
    content: |
      Results/outcomes

documents:
  - title: "Document title"
    file: /assets/documents/filename.pdf

tags:
  - tag1
  - tag2
---

EXTRACTION INSTRUCTIONS:
1. Extract project title and create brief description
2. Generate permalink from title
3. Identify category (projekty, zabytkowe, szkolenia)
4. Extract project metadata:
   - Client name
   - Location (city, województwo)
   - Year
   - Scope/type of work
   - Area (if mentioned)
   - Status (in progress, completed, concept)
5. Extract all gallery images with descriptions
6. Parse content sections:
   - Intro paragraph
   - Main description
   - Challenges (if present)
   - Solutions (if present)
   - Results/outcomes (if present)
7. Extract any linked PDF documents
8. Generate relevant tags from content
9. Convert all image URLs to relative paths

HTML INPUT:
{HTML_CONTENT_HERE}

OUTPUT (YAML ONLY):
```

### Blog/News Post Extraction Prompt

```markdown
TASK: Extract content from an IKROPKA blog/news post into YAML format.

PAGE TYPE: Blog/news post
LAYOUT: post

SCHEMA TO FOLLOW:
---
layout: post
title: "Post title"
description: "Post summary (1-2 sentences)"
date: 2025-10-15 # YYYY-MM-DD
author: "IKROPKA"
permalink: /aktualnosci/post-slug/

categories:
  - aktualności
  - category2

tags:
  - tag1
  - tag2

featured_image: /assets/images/news/image.jpg
featured_image_alt: "Image description"

sections:
  - type: intro
    content: |
      Opening paragraph

  - type: body
    content: |
      Main article text

  - type: quote
    text: "Quote text"
    author: "Attribution"

  - type: image
    image: /assets/images/news/photo.jpg
    alt: "Photo description"
    caption: "Optional caption"

  - type: conclusion
    content: |
      Closing paragraph

related:
  - type: service
    slug: "service-slug"
  - type: project
    slug: "project-slug"
---

EXTRACTION INSTRUCTIONS:
1. Extract post title
2. Create brief summary (1-2 sentences)
3. Extract publication date (convert to YYYY-MM-DD format)
4. Generate permalink from title and date
5. Identify categories and tags
6. Extract featured image
7. Parse article content into sections:
   - Intro paragraph
   - Body text (can be multiple paragraphs in one section)
   - Quotes (if present)
   - Embedded images (if present)
   - Conclusion
8. Extract related content links (to services or projects)
9. Preserve Polish text exactly

HTML INPUT:
{HTML_CONTENT_HERE}

OUTPUT (YAML ONLY):
```

### About Page Extraction Prompt

```markdown
TASK: Extract content from the IKROPKA "About Us" page into YAML format.

PAGE TYPE: About/Static page
LAYOUT: page

SCHEMA TO FOLLOW:
---
layout: page
title: "O nas"
description: "About IKROPKA landscape architecture studio"
permalink: /o-nas/

sections:
  - type: intro
    heading: "Heading"
    content: |
      Company overview

  - type: founder
    heading: "Studio leader"
    name: "Name"
    credentials:
      - "Credential 1"
      - "Credential 2"
    bio: |
      Founder bio

  - type: three_pillars
    heading: "Our services"
    items:
      - title: "Service"
        description: "Description"

  - type: expertise
    heading: "Our philosophy"
    content: |
      Approach and values

  - type: credentials_gallery
    heading: "Qualifications"
    images:
      - image: /assets/images/credentials/cert.jpg
        alt: "Certificate name"
        caption: "Optional"

  - type: stats
    heading: "Our achievements"
    items:
      - number: "1110"
        label: "Label"

  - type: partnerships
    heading: "Partnerships"
    content: |
      Partner description
    logos:
      - image: /assets/images/partners/logo.jpg
        alt: "Partner name"
---

EXTRACTION INSTRUCTIONS:
1. Extract page title ("O nas")
2. Create SEO description
3. Parse content sections:
   - Company overview/intro
   - Founder info (name, credentials, bio)
   - Three pillars of activity
   - Expertise/philosophy section
   - Credentials gallery (certificates)
   - Statistics (4 metrics)
   - Partnerships section with logos
4. Extract all images with alt text
5. Preserve structure and hierarchy

HTML INPUT:
{HTML_CONTENT_HERE}

OUTPUT (YAML ONLY):
```

---

## Edge Cases Handling

For all page types, if you encounter:

1. **Unrecognized HTML elements:**
```yaml
- type: html_block
  content: |
    <raw HTML here>
```

2. **Embedded videos/iframes:**
```yaml
- type: embed
  embed_type: youtube # or vimeo, iframe
  url: "URL"
  title: "Title"
```

3. **WordPress shortcodes:**
```yaml
- type: shortcode
  shortcode_name: "name"
  attributes:
    key: "value"
  note: "Manual conversion needed"
```

4. **Forms:**
```yaml
- type: contact_form
  note: "Contact Form 7 detected - deferred to Phase 2/3"
  original_shortcode: "[shortcode]"
```

---

## Validation Checklist

Before outputting YAML, verify:
- ✅ Valid YAML syntax (proper indentation, quoted strings when needed)
- ✅ All frontmatter fields present
- ✅ All sections have correct `type` field
- ✅ Image paths use /assets/images/ prefix
- ✅ Multi-line text uses `|` delimiter
- ✅ No HTML tags in plain text fields (unless in html_block)
- ✅ Dates in YYYY-MM-DD format
- ✅ Permalinks start with `/` and end with `/`
- ✅ Polish characters preserved correctly

---

**Usage:** Select the appropriate prompt for the page type, replace `{HTML_CONTENT_HERE}` with the actual HTML, and send to Kimi K2.5 via OpenRouter API.
