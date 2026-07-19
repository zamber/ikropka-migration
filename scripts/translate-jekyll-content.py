#!/usr/bin/env python3
"""
Translate Jekyll markdown files from Polish to English/German using OpenRouter API.

Preserves Jekyll frontmatter metadata (dates, permalinks, categories, image paths)
while translating content and translatable frontmatter fields.

Usage:
    python translate-jekyll-content.py \\
        --input docs/_portfolio/project.md \\
        --target-lang en \\
        --output docs/en/_portfolio/ \\
        --glossary scripts/translation-glossary.yaml \\
        --api-key YOUR_KEY
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, Tuple

import requests
import yaml

# OpenRouter API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "tencent/hy3:free"  # Tencent HY3 - free tier, good for translations

LANG_NAMES = {
    "en": "English",
    "de": "German"
}


def load_glossary(glossary_path: str) -> Dict:
    """Load translation glossary from YAML file."""
    with open(glossary_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_jekyll_file(filepath: str) -> Tuple[Dict, str]:
    """
    Parse Jekyll markdown file into frontmatter and content.

    Returns:
        (frontmatter_dict, content_str)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse Jekyll frontmatter (--- ... ---)
    if content.startswith('---\n'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            content_body = parts[2].strip()
            return frontmatter, content_body

    return {}, content


def format_glossary_for_prompt(glossary: Dict, target_lang: str) -> str:
    """Format glossary as a readable string for AI prompt."""
    lines = []

    for category, terms in glossary.items():
        if category == 'proper_nouns':
            continue  # Skip proper nouns section

        lines.append(f"\n{category.upper().replace('_', ' ')}:")

        for polish_term, translations in terms.items():
            if target_lang in translations:
                target_term = translations[target_lang]
                lines.append(f"  - {polish_term} → {target_term}")

    return "\n".join(lines)


def build_translation_prompt(content: str, target_lang: str, glossary: Dict) -> str:
    """Build system prompt for translation."""
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    glossary_text = format_glossary_for_prompt(glossary, target_lang)

    # Extract proper nouns from glossary
    proper_nouns = glossary.get('proper_nouns', [])
    proper_nouns_text = "\n  - ".join(proper_nouns) if proper_nouns else "N/A"

    return f"""You are an expert translator specializing in landscape architecture and dendrology.

Translate the following Polish text to {lang_name}.

CRITICAL RULES:
1. Preserve ALL markdown formatting exactly (##, **, *, >, -)
2. Preserve ALL Jekyll/Liquid template tags like {{% include %}} and {{{{ site.baseurl }}}}
3. Preserve ALL URLs and file paths unchanged (/assets/images/..., /portfolio/...)
4. Never translate proper nouns: company names, person names, city names, street names
5. Use specialized terminology from the glossary provided below
6. Maintain professional, formal tone appropriate for landscape architecture
7. Output ONLY the translated content - no explanations, no preamble, no markdown code blocks
8. Keep all numbers, dates, measurements unchanged (they will be formatted separately)

TRANSLATION GLOSSARY (Polish → {lang_name}):
{glossary_text}

PROPER NOUNS TO NEVER TRANSLATE:
  - {proper_nouns_text}

Additionally, preserve these patterns:
  - City names: Wrocław, Warszawa, Kraków, Poznań, etc.
  - Street names: al. Paderewskiego, ul. Grabiszyńska, etc.
  - Park names: Park Centralny, etc.
  - Company names: IKROPKA, Fundacja EkoRozwoju, Gmina Wrocław, etc.
  - Person names: Piotr Zaborowski, etc.

TEXT TO TRANSLATE:
{content}

TRANSLATION ({lang_name}):"""


def translate_via_api(content: str, target_lang: str, glossary: Dict, api_key: str) -> str:
    """Translate content using OpenRouter API with retry logic."""
    import time

    prompt = build_translation_prompt(content, target_lang, glossary)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/zamber/ikropka-migration",
        "X-Title": "IKROPKA Migration Translation"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,  # Low for consistency
        "max_tokens": 16000,
    }

    print(f"  → Sending to OpenRouter API ({MODEL})...")

    # Retry logic for rate limits
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(
                OPENROUTER_API_URL,
                json=payload,
                headers=headers,
                timeout=120
            )

            if response.status_code == 429:
                # Rate limited - wait and retry
                wait_time = 2 ** attempt * 10  # Exponential backoff: 10s, 20s, 40s, 80s, 160s
                print(f"  → Rate limited. Waiting {wait_time}s before retry {attempt+1}/{max_retries}...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            translated = response.json()["choices"][0]["message"]["content"].strip()

            # Clean up any markdown code blocks if AI added them
            translated = re.sub(r"^```.*?\n", "", translated, flags=re.MULTILINE)
            translated = re.sub(r"\n```$", "", translated, flags=re.MULTILINE)

            return translated

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429 and attempt < max_retries - 1:
                wait_time = 2 ** attempt * 10
                print(f"  → Rate limited. Waiting {wait_time}s before retry {attempt+1}/{max_retries}...")
                time.sleep(wait_time)
                continue
            else:
                raise

    raise Exception(f"Failed after {max_retries} retries due to rate limits")


def translate_frontmatter_field(text: str, target_lang: str, glossary: Dict, api_key: str) -> str:
    """Translate a single frontmatter field (short text)."""
    if not text or len(text.strip()) == 0:
        return text

    # Build simplified prompt for short text
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    glossary_text = format_glossary_for_prompt(glossary, target_lang)

    prompt = f"""Translate this Polish text to {lang_name}.

Use these specialized terms:
{glossary_text}

Do not translate: company names, person names, city names, street names.

Polish text: {text}

{lang_name} translation (output ONLY the translation, nothing else):"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 500,
    }

    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers, timeout=60)

    if response.status_code != 200:
        print(f"ERROR: API returned {response.status_code}")
        print(f"Response: {response.text}")

    response.raise_for_status()

    translated = response.json()["choices"][0]["message"]["content"].strip()

    # Remove quotes if AI added them
    translated = translated.strip('"').strip("'")

    return translated


def update_permalink_for_language(permalink: str, target_lang: str) -> str:
    """Update permalink to include language prefix."""
    if not permalink:
        return permalink

    # Add language prefix: /portfolio/slug/ → /en/portfolio/slug/
    if permalink.startswith('/'):
        return f"/{target_lang}{permalink}"
    else:
        return f"/{target_lang}/{permalink}"


def translate_tags_categories(items: list, target_lang: str, glossary: Dict, api_key: str) -> list:
    """Translate list of tags or categories."""
    if not items:
        return items

    translated = []
    for item in items:
        # Try to find in glossary first
        found = False
        for category, terms in glossary.items():
            if category == 'proper_nouns':
                continue
            for pl_term, translations in terms.items():
                if pl_term.lower() == item.lower() and target_lang in translations:
                    translated.append(translations[target_lang])
                    found = True
                    break
            if found:
                break

        if not found:
            # Translate via API
            trans = translate_frontmatter_field(item, target_lang, glossary, api_key)
            translated.append(trans)

    return translated


def translate_frontmatter(frontmatter: Dict, target_lang: str, glossary: Dict, api_key: str) -> Dict:
    """Translate translatable frontmatter fields."""
    new_frontmatter = frontmatter.copy()

    # Add language identifier
    new_frontmatter['lang'] = target_lang

    # Update permalink
    if 'permalink' in new_frontmatter:
        new_frontmatter['permalink'] = update_permalink_for_language(
            new_frontmatter['permalink'],
            target_lang
        )

    # Translate: title
    if 'title' in new_frontmatter and new_frontmatter['title']:
        print(f"  → Translating title...")
        new_frontmatter['title'] = translate_frontmatter_field(
            new_frontmatter['title'],
            target_lang,
            glossary,
            api_key
        )

    # Translate: description
    if 'description' in new_frontmatter and new_frontmatter['description']:
        print(f"  → Translating description...")
        new_frontmatter['description'] = translate_frontmatter_field(
            new_frontmatter['description'],
            target_lang,
            glossary,
            api_key
        )

    # Translate: tags (if user chose to translate them)
    if 'tags' in new_frontmatter and isinstance(new_frontmatter['tags'], list):
        print(f"  → Translating tags...")
        new_frontmatter['tags'] = translate_tags_categories(
            new_frontmatter['tags'],
            target_lang,
            glossary,
            api_key
        )

    # Translate: categories (if user chose to translate them)
    if 'categories' in new_frontmatter and isinstance(new_frontmatter['categories'], list):
        print(f"  → Translating categories...")
        new_frontmatter['categories'] = translate_tags_categories(
            new_frontmatter['categories'],
            target_lang,
            glossary,
            api_key
        )

    # Translate: gallery alt text
    if 'gallery' in new_frontmatter and isinstance(new_frontmatter['gallery'], list):
        print(f"  → Translating gallery alt text...")
        for item in new_frontmatter['gallery']:
            if 'alt' in item and item['alt']:
                item['alt'] = translate_frontmatter_field(
                    item['alt'],
                    target_lang,
                    glossary,
                    api_key
                )
            if 'caption' in item and item['caption']:
                item['caption'] = translate_frontmatter_field(
                    item['caption'],
                    target_lang,
                    glossary,
                    api_key
                )

    # Translate: project metadata (if present)
    if 'project' in new_frontmatter and isinstance(new_frontmatter['project'], dict):
        print(f"  → Translating project metadata...")
        project = new_frontmatter['project']

        # Translate: status
        if 'status' in project and project['status']:
            project['status'] = translate_frontmatter_field(
                project['status'],
                target_lang,
                glossary,
                api_key
            )

        # Translate: scope
        if 'scope' in project and project['scope']:
            project['scope'] = translate_frontmatter_field(
                project['scope'],
                target_lang,
                glossary,
                api_key
            )

        # Translate location voivodeship (partial)
        if 'location' in project and project['location']:
            loc = project['location']
            # Try to find voivodeship pattern and translate
            for pl_voiv, translations in glossary.get('voivodeships', {}).items():
                if pl_voiv in loc and target_lang in translations:
                    loc = loc.replace(pl_voiv, translations[target_lang])
            project['location'] = loc

    return new_frontmatter


def save_jekyll_file(frontmatter: Dict, content: str, output_path: str):
    """Save translated Jekyll markdown file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        f.write("---\n\n")
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Translate Jekyll markdown files")
    parser.add_argument('--input', required=True, help='Input Jekyll markdown file (Polish)')
    parser.add_argument('--target-lang', required=True, choices=['en', 'de'], help='Target language')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--glossary', required=True, help='Path to translation glossary YAML')
    parser.add_argument('--api-key', help='OpenRouter API key (or set OPENROUTER_API_KEY env var)')

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print("ERROR: OpenRouter API key not provided (use --api-key or OPENROUTER_API_KEY env var)")
        sys.exit(1)

    # Load inputs
    print(f"Loading {args.input}...")
    frontmatter, content = load_jekyll_file(args.input)

    print(f"Loading glossary from {args.glossary}...")
    glossary = load_glossary(args.glossary)

    # Translate frontmatter
    print(f"Translating frontmatter to {args.target_lang}...")
    translated_frontmatter = translate_frontmatter(frontmatter, args.target_lang, glossary, api_key)

    # Translate content
    print(f"Translating content to {args.target_lang}...")
    translated_content = translate_via_api(content, args.target_lang, glossary, api_key)

    # Save output
    input_filename = Path(args.input).name
    output_path = Path(args.output) / input_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Saving to {output_path}...")
    save_jekyll_file(translated_frontmatter, translated_content, str(output_path))

    print(f"✅ Translation complete: {output_path}")


if __name__ == '__main__':
    main()
