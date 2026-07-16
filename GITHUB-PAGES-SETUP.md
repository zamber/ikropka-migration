# GitHub Pages Deployment Instructions

**Status:** Ready to deploy! ✅

---

## Step 1: Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/zamber/ikropka-migration

2. Click on **Settings** (top right of repo page)

3. In the left sidebar, scroll down and click **Pages**

4. Under **"Build and deployment"**, configure:
   - **Source:** Deploy from a branch
   - **Branch:** `main`
   - **Folder:** `/docs`

5. Click **Save**

6. Wait 2-3 minutes for the first build to complete

## Step 2: Verify Deployment

Once the build completes, your site will be available at:

**🔗 https://zamber.github.io/ikropka-migration/**

You'll see a green checkmark and a "Visit site" button when it's ready.

## Step 3: Check Build Status

- GitHub will show build status at the top of the Pages settings
- You can also check the **Actions** tab to see the build log
- If there are errors, the Actions log will show what failed

---

## Configuration Details

The site is already configured correctly:

```yaml
# _config.yml
url: "https://zamber.github.io"
baseurl: "/ikropka-migration"
repository: "zamber/ikropka-migration"
```

**✅ All set!** GitHub Pages will build Jekyll automatically using:
- Jekyll 4.x (latest supported by GitHub Pages)
- Minimal Mistakes theme
- All plugins defined in Gemfile

---

## What to Expect

### First Build
- **Time:** 2-3 minutes
- **Process:** GitHub Actions will install Jekyll, build the site, and deploy

### Site Structure
- **Homepage:** `https://zamber.github.io/ikropka-migration/`
- **Portfolio:** `https://zamber.github.io/ikropka-migration/portfolio/`
- **Services:** `https://zamber.github.io/ikropka-migration/oferta/`
- **About:** `https://zamber.github.io/ikropka-migration/o-nas/`
- **Contact:** `https://zamber.github.io/ikropka-migration/kontakt/`

### Content
- **3 pages** (homepage, about, contact)
- **13 services** (dendrology & design)
- **72 portfolio projects** (case studies)
- **64 blog posts** (news & updates)
- **696 optimized images** (WebP + JPEG)

---

## Troubleshooting

### If Build Fails

1. **Check Actions tab** for error details
2. **Common issues:**
   - Missing gems → GitHub Pages installs automatically
   - Theme issues → Minimal Mistakes is GitHub Pages compatible
   - Image paths → Should work (relative paths `/assets/images/`)
   - Markdown syntax → Should be fine (we validated during conversion)

### If Site Looks Broken

1. **Check browser console** for 404 errors
2. **Verify baseurl** in links (all paths should start with `/ikropka-migration/`)
3. **Check image loading** (may need to add `{{ site.baseurl }}` prefix)

### If Images Don't Load

Images are referenced as `/assets/images/filename.webp` in markdown.

Jekyll should automatically prefix with baseurl, but if they 404, we may need to update paths to:
```liquid
{{ site.baseurl }}/assets/images/filename.webp
```

---

## Next Steps After Deployment

Once the site is live:

1. ✅ **Verify homepage renders** - Check hero section, content sections
2. ✅ **Test portfolio page** - Should list all 72 projects
3. ✅ **Test service pages** - Check 13 service detail pages
4. ✅ **Test image loading** - Verify images display (696 files)
5. ✅ **Check navigation** - Test all menu links work
6. ✅ **Mobile test** - View on phone/tablet
7. ✅ **Performance check** - Run Lighthouse audit

Then we can proceed with **Milestone 6** (Portfolio features) if everything looks good!

---

## Notes

- GitHub Pages builds automatically on every push to `main`
- Build logs available in Actions tab
- Site updates in 1-2 minutes after push
- This is a **private repository** - GitHub Pages works with private repos on paid plans
- Ensure your GitHub account has Pages enabled for private repos (Pro/Team/Enterprise)

**Ready to go! 🚀** Just enable Pages in the repo settings.
