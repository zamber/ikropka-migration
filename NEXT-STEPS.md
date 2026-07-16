# Next Steps for IKROPKA Migration

## Current Status: Milestone 4 Complete ✅

**What's Done:**
- ✅ Milestone 1: Project Setup & Analysis
- ✅ Milestone 2: Jekyll Scaffolding (Minimal Mistakes theme configured)
- ✅ Milestone 3: Image Migration (364 images → 696 optimized files, 101MB)
- ✅ Milestone 4: Content Extraction Framework (scripts, schemas, prompts ready)

## Blocker: OpenRouter API Key

**Issue:** The existing OpenRouter API key (`sk-or-v1-...f26dd9`) is **expired/unfunded**.

```bash
# Attempted homepage extraction:
python3 scripts/extract-content.py \
  --url https://ikropka.eu/ \
  --type homepage \
  --output content-structured/test/homepage-v1.yaml

# Result: 401 Unauthorized
```

**Root Cause:** According to OpenClaw session logs, OpenRouter has been failing since March 2026 with:
- `402 "requires more credits"` errors (weekly limit exhausted)
- `404` errors when `google/gemini-2.0-flash-001` was deprecated

The key hasn't been refilled since then.

## How to Continue

### Option 1: Get New/Refilled OpenRouter API Key (Recommended)

**Cost:** ~$1.05 total for 150 pages (very affordable)
- Kimi K2.5: $0.375/1M input, $2.025/1M output
- Estimated: ~$0.006 per page × 150 pages + refinement iterations

**Steps:**
1. Visit https://openrouter.ai/
2. Log in (or create account if needed)
3. Go to Settings → Keys
4. Either:
   - **Refill the weekly limit** on existing key (`...f26dd9`)
   - **Create a new API key** with sufficient credits

5. Export the key:
   ```bash
   export OPENROUTER_API_KEY='your-key-here'
   ```

6. **Test the extraction:**
   ```bash
   cd /home/luna/ikropka-migration
   python3 scripts/extract-content.py \
     --url https://ikropka.eu/ \
     --type homepage \
     --output content-structured/test/homepage-v1.yaml
   ```

7. **Review the output:**
   ```bash
   cat content-structured/test/homepage-v1.yaml
   yamllint content-structured/test/homepage-v1.yaml  # validate syntax
   ```

8. **Refine the prompt if needed** (edit `scripts/extraction-prompt-template.md`)

9. **Continue with remaining 4 test pages:**
   - About page: https://ikropka.eu/o-nas/
   - Service page: https://ikropka.eu/oferta/inwentaryzacje-dendrologiczne/
   - Portfolio: https://ikropka.eu/projekt/rewaloryzacja-zabytkowej-alei-projekt-poprawy-warunkow-siedliskowych-przy-al-paderewskiego/
   - Blog post: https://ikropka.eu/posiadamy-nowe-uprawnienia-branzowe-ett-european-tree-technician-ekspert-arborysta-dendrolog/

10. **Only after all 5 pass cleanly:** Proceed to Milestone 5 (batch processing ~145 pages)

### Option 2: Use Alternative AI Service

If OpenRouter is unavailable, the extraction script could be adapted to use:
- **Anthropic Claude API** (requires modification to use Claude directly)
- **OpenAI GPT-4** (requires script changes)
- **Local LLM** (Ollama, LM Studio) - slower but no API costs

**Trade-off:** Would require modifying `scripts/extract-content.py` to support a different API.

### Option 3: Manual Content Migration (Not Recommended)

Manually copy/paste content from WordPress → Jekyll YAML for all 150 pages.

**Estimated time:** 2-4 weeks of tedious work
**Risk:** High chance of errors, inconsistency, content loss

---

## Refinement Loop Process (Once API Key Works)

**Goal:** Get all 5 test pages extracting cleanly (zero manual fixes).

**For each test page:**

1. **Run extraction**
2. **Review output** - check for:
   - Valid YAML syntax?
   - All content extracted?
   - Correct section types?
   - Images with paths/alt text?
   - No data loss?
3. **If issues found:**
   - Edit `scripts/extraction-prompt-template.md`
   - Add clarifications, examples, edge case handling
   - Re-run extraction
4. **Repeat until clean**

**Success criteria:**
- ✅ All 5 test pages extract without errors
- ✅ Zero manual editing required
- ✅ Content maps directly to Jekyll

**Only then:** Proceed to Milestone 5 (batch process remaining ~145 pages)

---

## What's Ready to Use (No Blocker)

Everything except the AI extraction:

1. **Jekyll site** (`site/`) - fully configured, can be previewed:
   ```bash
   cd /home/luna/ikropka-migration/site
   bundle exec jekyll serve
   # Visit: http://localhost:4000/ikropka-migration/
   ```

2. **Optimized images** (`site/assets/images/`) - 696 files ready to use

3. **Extraction framework** - fully documented and tested (except for the live API call)

4. **Project documentation:**
   - `CLAUDE.md` - project guidance
   - `MEMORY.md` - decisions and progress log
   - `ROADMAP.md` - full Phase 1-4 plan
   - `scripts/README.md` - extraction workflow
   - `scripts/yaml-schema.md` - YAML structure for all page types
   - `scripts/TEST-PAGES.md` - 5 test pages selected

---

## Summary

**The extraction framework is complete and ready to use.**

**To continue:** Get a funded OpenRouter API key ($1-2), then run the refinement loop on 5 test pages.

**Estimated time to complete Phase 1:** 1-2 weeks after API key is available (assuming 3-5 days for refinement + 3-5 days for batch processing + Jekyll integration).

---

**Last Updated:** 2026-07-16
**Current Milestone:** 4 (Framework Complete, Blocked on API Key)
**Next Milestone:** 4 (Refinement Loop) → 5 (Batch Processing) → 6-10 (Jekyll Integration, Features, QA)
