# Content Extraction Scripts

This directory contains scripts and configuration for extracting content from ikropka.eu WordPress site and converting it to Jekyll-compatible YAML.

## Files

### Core Scripts
- **`extract-content.py`** - Main Python script that uses OpenRouter API (Kimi K2.5) to convert HTML → YAML
- **`download-images-via-api.py`** - Downloads images from WordPress REST API (already complete)
- **`deduplicate-wp-thumbnails.js`** - Deduplicates WordPress thumbnail images (already complete)
- **`optimize-images.sh`** - Optimizes images to WebP + JPEG (already complete)

### Configuration
- **`TEST-PAGES.md`** - List of 5 test pages for refinement loop
- **`yaml-schema.md`** - Complete YAML schema documentation for all page types
- **`extraction-prompt-template.md`** - Prompts used with AI model for each page type

## Content Extraction Workflow

### Prerequisites

1. **OpenRouter API Key**
   - Visit https://openrouter.ai/
   - Sign up / Log in
   - Create an API key
   - Export it: `export OPENROUTER_API_KEY='your-key-here'`

2. **Python Dependencies**
   ```bash
   pip install requests pyyaml
   ```

3. **YAML Validator (optional but recommended)**
   ```bash
   pip install yamllint
   # or
   npm install -g js-yaml
   ```

### Usage

#### Basic Extraction

**From URL:**
```bash
python scripts/extract-content.py \
  --url https://ikropka.eu/ \
  --type homepage \
  --output content-structured/homepage.yaml
```

**From local HTML file:**
```bash
python scripts/extract-content.py \
  --html scraped-content/homepage.html \
  --type service \
  --output content-structured/service-page.yaml
```

#### Page Types

- `homepage` - Homepage with hero slider, sections, testimonials
- `about` - About page (O nas)
- `service` - Service detail pages (14 pages in /oferta/)
- `portfolio` - Portfolio project pages (130+ pages)
- `post` - Blog/news posts (Aktualności)

### Refinement Loop (Milestone 4)

**Goal:** Refine the extraction prompt until zero manual fixes are needed.

#### Process:

1. **Select test page** (from `TEST-PAGES.md`)

2. **Run extraction:**
   ```bash
   python scripts/extract-content.py \
     --url https://ikropka.eu/ \
     --type homepage \
     --output test-output/homepage-v1.yaml
   ```

3. **Review output manually:**
   ```bash
   # Validate YAML syntax
   yamllint test-output/homepage-v1.yaml

   # Read the file
   cat test-output/homepage-v1.yaml
   ```

4. **Check for issues:**
   - ✅ Valid YAML syntax?
   - ✅ All important content extracted?
   - ✅ Correct section types identified?
   - ✅ Images extracted with paths/alt text?
   - ✅ Proper structure for Jekyll?
   - ✅ No content loss?

5. **If issues found:**
   - Edit `extraction-prompt-template.md` to add clarifications
   - Or edit `yaml-schema.md` if structure needs adjustment
   - Re-run extraction: `--output test-output/homepage-v2.yaml`
   - Compare versions: `diff test-output/homepage-v1.yaml test-output/homepage-v2.yaml`

6. **Repeat until clean** (zero manual fixes needed)

7. **Move to next test page**

#### Success Criteria (before batch processing)

All 5 test pages must achieve:
- ✅ Valid YAML syntax
- ✅ Zero content loss
- ✅ Correct structure
- ✅ No manual editing required
- ✅ Ready for Jekyll integration

### Batch Processing (Milestone 5)

**Only proceed after refinement loop succeeds on all 5 test pages.**

```bash
# Create batch script to process all ~150 pages
for url in $(cat page-urls.txt); do
  slug=$(echo "$url" | sed 's|https://ikropka.eu/||' | sed 's|/$||' | tr '/' '-')
  python scripts/extract-content.py \
    --url "$url" \
    --type auto-detect \
    --output "content-structured/${slug}.yaml"
done
```

## Tips & Troubleshooting

### Common Issues

**1. API Rate Limits**
- Kimi K2.5 pricing: $0.375/1M input, $2.025/1M output
- Budget: ~$0.89 for 150 pages (estimated)
- Add delays between requests if needed: `sleep 2`

**2. Large HTML Pages**
- If HTML > 200KB, consider cleaning more aggressively
- Remove navigation, footer, sidebar before sending to API

**3. YAML Syntax Errors**
- Usually caused by unescaped special characters
- Check for unquoted colons, brackets, or quotes in strings
- Validate with: `yamllint file.yaml`

**4. Content Loss**
- Compare original HTML with extracted YAML
- Check if sections were skipped or mis-identified
- Refine prompt to be more explicit about what to extract

**5. Incorrect Section Types**
- Review `yaml-schema.md` and ensure types are well-defined
- Add examples to the prompt template
- Use `html_block` type as fallback for unrecognized content

### Cost Estimation

**Kimi K2.5 Pricing:**
- Input: $0.375 per 1M tokens
- Output: $2.025 per 1M tokens

**Estimated costs:**
- Per page: ~$0.006 (1000 input tokens + 2000 output tokens)
- 150 pages: ~$0.90 total
- With refinement (5 test pages × 5 iterations): ~$0.15
- **Total budget: ~$1.05**

### Best Practices

1. **Start with simple pages** (About, Blog posts) to refine prompts
2. **Test incrementally** - don't batch process until refinement succeeds
3. **Version your outputs** (`-v1.yaml`, `-v2.yaml`) during refinement
4. **Keep original HTML** for reference and re-runs
5. **Commit progress** frequently during refinement loop
6. **Document issues** in MEMORY.md for future reference

---

## Directory Structure

```
scripts/
├── README.md                          # This file
├── TEST-PAGES.md                      # 5 test pages for refinement
├── yaml-schema.md                     # YAML structure documentation
├── extraction-prompt-template.md      # AI prompts for each page type
├── extract-content.py                 # Main extraction script
├── download-images-via-api.py         # Image download (complete)
├── deduplicate-wp-thumbnails.js       # Deduplication (complete)
└── optimize-images.sh                 # Optimization (complete)

content-structured/                     # Output directory for extracted YAML
├── homepage.yaml
├── o-nas.yaml
├── oferta/
│   ├── inwentaryzacje-dendrologiczne.yaml
│   └── ...
├── portfolio/
│   ├── projekt-1.yaml
│   └── ...
└── aktualnosci/
    ├── post-1.yaml
    └── ...

test-output/                            # Refinement loop test outputs
├── homepage-v1.yaml
├── homepage-v2.yaml
└── ...
```

---

**Last Updated:** 2026-07-16
**Status:** Ready for refinement loop (Milestone 4)
