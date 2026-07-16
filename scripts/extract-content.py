#!/usr/bin/env python3
"""
Content extraction script for IKROPKA WordPress → Jekyll migration.

Uses OpenRouter API with Kimi K2.5 model to convert HTML pages to structured YAML.

Usage:
    python extract-content.py --url https://ikropka.eu/ --type homepage --output output.yaml
    python extract-content.py --html input.html --type service --output output.yaml
"""

import argparse
import os
import sys
import re
import requests
from pathlib import Path

# OpenRouter API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "moonshotai/kimi-k2.7-code"  # Kimi K2.7 Code model (latest available)

# Prompt templates directory
SCRIPT_DIR = Path(__file__).parent
PROMPT_TEMPLATE_FILE = SCRIPT_DIR / "extraction-prompt-template.md"


def load_prompt_template(page_type: str) -> str:
    """Load the extraction prompt for a specific page type."""
    with open(PROMPT_TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Extract the relevant prompt section for the page type
    type_map = {
        "homepage": "Homepage Extraction Prompt",
        "about": "About Page Extraction Prompt",
        "service": "Service Page Extraction Prompt",
        "portfolio": "Portfolio Project Extraction Prompt",
        "post": "Blog/News Post Extraction Prompt",
    }

    if page_type not in type_map:
        raise ValueError(f"Unknown page type: {page_type}. Must be one of: {', '.join(type_map.keys())}")

    section_title = type_map[page_type]

    # Find the section in the template
    pattern = rf"### {re.escape(section_title)}.*?```markdown\n(.*?)```"
    match = re.search(pattern, template_content, re.DOTALL)

    if not match:
        raise ValueError(f"Could not find prompt section for: {section_title}")

    return match.group(1).strip()


def fetch_html_from_url(url: str) -> str:
    """Fetch HTML content from a URL."""
    print(f"Fetching HTML from: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; IKROPKA-Migration/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def load_html_from_file(filepath: str) -> str:
    """Load HTML content from a file."""
    print(f"Loading HTML from: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def clean_html(html: str) -> str:
    """Clean and prepare HTML for extraction."""
    # Remove script tags and their content
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Remove style tags and their content
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Remove comments
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    return html.strip()


def extract_content_with_ai(html: str, page_type: str, api_key: str) -> str:
    """
    Send HTML to OpenRouter API (Kimi K2.5) and get YAML output.
    """
    prompt_template = load_prompt_template(page_type)

    # Replace placeholder with actual HTML
    prompt = prompt_template.replace("{HTML_CONTENT_HERE}", html)

    print(f"Sending request to OpenRouter API (model: {MODEL})...")
    print(f"HTML size: {len(html)} chars, Prompt size: {len(prompt)} chars")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/zamber/ikropka-migration",
        "X-Title": "IKROPKA Migration"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": """You are an expert at extracting structured content from HTML and converting it to clean, valid YAML for Jekyll static sites.

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
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,  # Low temperature for consistency
        "max_tokens": 16000,  # Kimi K2.5 has high context, allow long outputs
    }

    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers, timeout=120)
    response.raise_for_status()

    result = response.json()

    if "choices" not in result or len(result["choices"]) == 0:
        raise ValueError(f"Unexpected API response: {result}")

    yaml_output = result["choices"][0]["message"]["content"].strip()

    # Remove markdown code blocks if AI added them (sometimes models do this)
    yaml_output = re.sub(r"^```ya?ml\n", "", yaml_output, flags=re.MULTILINE)
    yaml_output = re.sub(r"\n```$", "", yaml_output, flags=re.MULTILINE)

    return yaml_output


def save_yaml(yaml_content: str, output_path: str):
    """Save YAML content to a file."""
    print(f"Saving YAML to: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    print(f"✅ YAML saved successfully ({len(yaml_content)} chars)")


def main():
    parser = argparse.ArgumentParser(description="Extract content from WordPress HTML to Jekyll YAML")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--url", help="URL to fetch HTML from")
    input_group.add_argument("--html", help="Path to HTML file")

    parser.add_argument("--type", required=True,
                       choices=["homepage", "about", "service", "portfolio", "post"],
                       help="Page type (determines which schema/prompt to use)")
    parser.add_argument("--output", required=True, help="Output YAML file path")
    parser.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY env var)")

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OpenRouter API key required. Provide via --api-key or OPENROUTER_API_KEY env var.")
        print("\nTo get an API key:")
        print("1. Visit https://openrouter.ai/")
        print("2. Sign up / Log in")
        print("3. Go to Keys section and create a new key")
        print("4. Export OPENROUTER_API_KEY='your-key-here' or use --api-key flag")
        sys.exit(1)

    try:
        # Load HTML
        if args.url:
            html = fetch_html_from_url(args.url)
        else:
            html = load_html_from_file(args.html)

        # Clean HTML
        html = clean_html(html)
        print(f"Cleaned HTML size: {len(html)} chars")

        # Extract content with AI
        yaml_content = extract_content_with_ai(html, args.type, api_key)

        # Save output
        save_yaml(yaml_content, args.output)

        print("\n✅ Extraction complete!")
        print(f"Next steps:")
        print(f"1. Review the YAML output: {args.output}")
        print(f"2. Validate YAML syntax: yamllint {args.output}")
        print(f"3. Check for missing content or structural issues")
        print(f"4. Refine prompt if needed and re-run")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
