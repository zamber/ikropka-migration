#!/usr/bin/env python3
"""
Convert extracted YAML files to Jekyll markdown format.

This script takes the structured YAML files from content-structured/ and converts them
to Jekyll-compatible markdown files with frontmatter + content.

Usage:
    python convert-yaml-to-jekyll.py
"""

import yaml
import os
from pathlib import Path
from datetime import datetime
import re

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
STRUCTURED_DIR = PROJECT_ROOT / "content-structured"
JEKYLL_SITE_DIR = PROJECT_ROOT / "site"

# Output directories
PAGES_DIR = JEKYLL_SITE_DIR / "_pages"
PORTFOLIO_DIR = JEKYLL_SITE_DIR / "_portfolio"
SERVICES_DIR = JEKYLL_SITE_DIR / "_services"
POSTS_DIR = JEKYLL_SITE_DIR / "_posts"


def slugify(text):
    """Convert text to URL-safe slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def load_yaml_file(yaml_file):
    """Load YAML file, handling Jekyll frontmatter format."""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

        # Handle Jekyll frontmatter format: --- yaml --- (optionally with content after)
        if content.startswith('---\n'):
            # Remove opening ---
            content = content[4:]

            # Find closing --- and extract only YAML part
            if '\n---' in content:
                # Split at first occurrence of \n---
                yaml_part = content.split('\n---')[0]
                return yaml.safe_load(yaml_part)
            else:
                # No closing ---, treat entire content as YAML
                return yaml.safe_load(content)
        else:
            # No frontmatter delimiters, treat as plain YAML
            return yaml.safe_load(content)


def convert_homepage(yaml_file, output_dir):
    """Convert homepage YAML to Jekyll markdown."""
    data = load_yaml_file(yaml_file)

    # Homepage goes to _pages/index.md
    output_file = output_dir / "index.md"

    # Build frontmatter
    frontmatter = {
        'layout': 'splash',  # Use splash layout for homepage
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'permalink': '/',
        'header': {},
    }

    # Add hero if exists
    if 'hero' in data and 'slides' in data['hero']:
        slides = data['hero']['slides']
        if slides:
            # Use first slide as header image
            frontmatter['header'] = {
                'overlay_image': slides[0]['image'],
                'overlay_filter': '0.5',
                'caption': slides[0].get('caption', ''),
            }

    # Build content from sections
    content_parts = []

    for section in data.get('sections', []):
        section_type = section.get('type', 'content')

        if section_type == 'intro':
            content_parts.append(f"## {section.get('heading', '')}\n\n{section.get('content', '')}\n")

        elif section_type == 'three_pillars':
            content_parts.append(f"## {section.get('heading', '')}\n\n")
            for item in section.get('items', []):
                content_parts.append(f"### {item.get('title', '')}\n\n")
                content_parts.append(f"{item.get('description', '')}\n\n")
                if item.get('link'):
                    content_parts.append(f"[Dowiedz się więcej]({item['link']})\n\n")

        elif section_type == 'content':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'strengths':
            content_parts.append(f"## {section.get('heading', '')}\n\n")
            for item in section.get('items', []):
                content_parts.append(f"- **{item.get('title', '')}**: {item.get('description', '')}\n")
            content_parts.append("\n")

        elif section_type == 'featured_projects':
            content_parts.append(f"## {section.get('heading', '')}\n\n")
            # Portfolio will be rendered via Jekyll includes
            content_parts.append("{% include portfolio-grid.html limit=6 %}\n\n")

        elif section_type == 'testimonials':
            content_parts.append(f"## {section.get('heading', '')}\n\n")
            for testimonial in section.get('items', []):
                content_parts.append(f"> {testimonial.get('quote', '')}\n>\n")
                content_parts.append(f"> — **{testimonial.get('author', '')}**, {testimonial.get('role', '')}\n\n")

    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
        f.write("---\n\n")
        f.write("".join(content_parts))

    print(f"✅ Converted: {yaml_file.name} → {output_file.relative_to(JEKYLL_SITE_DIR)}")


def convert_service(yaml_file, output_dir):
    """Convert service YAML to Jekyll markdown."""
    data = load_yaml_file(yaml_file)

    # Generate filename from permalink or title
    permalink = data.get('permalink', '')
    if permalink:
        slug = permalink.split('/')[-2]  # Extract slug from /oferta/slug/
    else:
        slug = slugify(data.get('title', yaml_file.stem))

    output_file = output_dir / f"{slug}.md"

    # Build frontmatter
    frontmatter = {
        'layout': 'single',
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'permalink': data.get('permalink', f'/oferta/{slug}/'),
        'category': data.get('category', 'services'),
        'service_type': data.get('service_type', ''),
    }

    # Build content from sections
    content_parts = []

    for section in data.get('sections', []):
        section_type = section.get('type', 'content')

        if section_type == 'intro':
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'description':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            if section.get('image'):
                content_parts.append(f"![{section.get('image_alt', '')}]({section['image']})\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'benefits' or section_type == 'services_list':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            for item in section.get('items', []):
                content_parts.append(f"- {item}\n")
            content_parts.append("\n")

        elif section_type == 'content':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
        f.write("---\n\n")
        f.write("".join(content_parts))

    print(f"✅ Converted: {yaml_file.name} → {output_file.relative_to(JEKYLL_SITE_DIR)}")


def convert_portfolio(yaml_file, output_dir):
    """Convert portfolio YAML to Jekyll markdown."""
    data = load_yaml_file(yaml_file)

    # Generate filename from permalink or title
    permalink = data.get('permalink', '')
    if permalink:
        slug = permalink.split('/')[-2]  # Extract slug from /portfolio/slug/
    else:
        slug = slugify(data.get('title', yaml_file.stem))

    output_file = output_dir / f"{slug}.md"

    # Build frontmatter
    frontmatter = {
        'layout': 'single',
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'permalink': data.get('permalink', f'/portfolio/{slug}/'),
        'category': data.get('category', 'projekty'),
        'featured_image': data.get('featured_image', ''),
    }

    # Add project metadata if exists
    if 'project_meta' in data:
        frontmatter['project'] = data['project_meta']

    # Add gallery if exists
    if 'gallery' in data:
        frontmatter['gallery'] = data['gallery']

    # Build content from sections
    content_parts = []

    # Add gallery at the top if exists
    if 'gallery' in data:
        content_parts.append("{% include gallery %}\n\n")

    for section in data.get('sections', []):
        section_type = section.get('type', 'content')

        if section_type == 'intro':
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'description':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'challenges':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'solution':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'results':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'content':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
        f.write("---\n\n")
        f.write("".join(content_parts))

    print(f"✅ Converted: {yaml_file.name} → {output_file.relative_to(JEKYLL_SITE_DIR)}")


def convert_post(yaml_file, output_dir):
    """Convert blog post YAML to Jekyll markdown."""
    data = load_yaml_file(yaml_file)

    # Extract date from permalink or use current date
    permalink = data.get('permalink', '')
    date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', permalink)
    if date_match:
        year, month, day = date_match.groups()
        date = f"{year}-{month}-{day}"
    else:
        # Use file modification time or current date
        date = datetime.now().strftime("%Y-%m-%d")

    # Generate filename from date + slug
    if permalink:
        slug = permalink.split('/')[-2]  # Extract slug
    else:
        slug = slugify(data.get('title', yaml_file.stem))

    output_file = output_dir / f"{date}-{slug}.md"

    # Build frontmatter
    frontmatter = {
        'layout': 'single',
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'date': date,
        'categories': data.get('categories', ['aktualności']),
        'tags': data.get('tags', []),
    }

    # Add featured image if exists
    if 'featured_image' in data:
        frontmatter['header'] = {
            'image': data['featured_image'],
            'teaser': data['featured_image'],
        }

    # Build content from sections
    content_parts = []

    for section in data.get('sections', []):
        section_type = section.get('type', 'content')

        if section_type == 'intro' or section_type == 'content':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
        f.write("---\n\n")
        f.write("".join(content_parts))

    print(f"✅ Converted: {yaml_file.name} → {output_file.relative_to(JEKYLL_SITE_DIR)}")


def convert_about_page(yaml_file, output_dir):
    """Convert about/contact pages to Jekyll markdown."""
    data = load_yaml_file(yaml_file)

    # Determine output file from permalink
    permalink = data.get('permalink', '')
    if '/o-nas' in permalink or 'about' in yaml_file.stem.lower():
        output_file = output_dir / "about.md"
    elif '/kontakt' in permalink or 'contact' in yaml_file.stem.lower():
        output_file = output_dir / "contact.md"
    else:
        # Generic page
        slug = slugify(data.get('title', yaml_file.stem))
        output_file = output_dir / f"{slug}.md"

    # Build frontmatter
    frontmatter = {
        'layout': 'single',
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'permalink': data.get('permalink', f'/{slugify(data.get("title", ""))}'),
    }

    # Build content from sections
    content_parts = []

    for section in data.get('sections', []):
        section_type = section.get('type', 'content')

        if section_type == 'intro' or section_type == 'content':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            content_parts.append(f"{section.get('content', '')}\n\n")

        elif section_type == 'team':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            for member in section.get('members', []):
                content_parts.append(f"### {member.get('name', '')}\n\n")
                if member.get('role'):
                    content_parts.append(f"**{member['role']}**\n\n")
                if member.get('bio'):
                    content_parts.append(f"{member['bio']}\n\n")

        elif section_type == 'contact_info':
            if section.get('heading'):
                content_parts.append(f"## {section.get('heading', '')}\n\n")
            info = section.get('info', {})
            if info.get('address'):
                content_parts.append(f"**Adres:**\n{info['address']}\n\n")
            if info.get('phone'):
                content_parts.append(f"**Telefon:**\n{info['phone']}\n\n")
            if info.get('email'):
                content_parts.append(f"**Email:**\n{info['email']}\n\n")

    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
        f.write("---\n\n")
        f.write("".join(content_parts))

    print(f"✅ Converted: {yaml_file.name} → {output_file.relative_to(JEKYLL_SITE_DIR)}")


def main():
    """Main conversion script."""
    print("🚀 Starting YAML → Jekyll conversion...\n")

    # Ensure output directories exist
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_DIR.mkdir(parents=True, exist_ok=True)
    SERVICES_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    stats = {'pages': 0, 'services': 0, 'portfolio': 0, 'posts': 0, 'errors': 0}

    # Convert homepage
    print("📄 Converting pages...")
    homepage_file = STRUCTURED_DIR / "pages" / "homepage.yaml"
    if homepage_file.exists():
        try:
            convert_homepage(homepage_file, PAGES_DIR)
            stats['pages'] += 1
        except Exception as e:
            print(f"❌ Error converting {homepage_file.name}: {e}")
            stats['errors'] += 1

    # Convert other pages (about, contact)
    for yaml_file in (STRUCTURED_DIR / "pages").glob("*.yaml"):
        if yaml_file.name == "homepage.yaml":
            continue
        try:
            convert_about_page(yaml_file, PAGES_DIR)
            stats['pages'] += 1
        except Exception as e:
            print(f"❌ Error converting {yaml_file.name}: {e}")
            stats['errors'] += 1

    # Convert services
    print("\n🛠️  Converting services...")
    for yaml_file in (STRUCTURED_DIR / "services").glob("*.yaml"):
        try:
            convert_service(yaml_file, SERVICES_DIR)
            stats['services'] += 1
        except Exception as e:
            print(f"❌ Error converting {yaml_file.name}: {e}")
            stats['errors'] += 1

    # Convert portfolio
    print("\n🎨 Converting portfolio...")
    for yaml_file in (STRUCTURED_DIR / "portfolio").glob("*.yaml"):
        try:
            convert_portfolio(yaml_file, PORTFOLIO_DIR)
            stats['portfolio'] += 1
        except Exception as e:
            print(f"❌ Error converting {yaml_file.name}: {e}")
            stats['errors'] += 1

    # Convert posts
    print("\n📰 Converting posts...")
    for yaml_file in (STRUCTURED_DIR / "posts").glob("*.yaml"):
        try:
            convert_post(yaml_file, POSTS_DIR)
            stats['posts'] += 1
        except Exception as e:
            print(f"❌ Error converting {yaml_file.name}: {e}")
            stats['errors'] += 1

    # Print summary
    print("\n" + "="*50)
    print("✅ Conversion Complete!")
    print("="*50)
    print(f"Pages:     {stats['pages']}")
    print(f"Services:  {stats['services']}")
    print(f"Portfolio: {stats['portfolio']}")
    print(f"Posts:     {stats['posts']}")
    print(f"Errors:    {stats['errors']}")
    print(f"TOTAL:     {sum(v for k, v in stats.items() if k != 'errors')}")
    print("="*50)


if __name__ == "__main__":
    main()
