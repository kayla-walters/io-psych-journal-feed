# Deployment Checklist

Use this as a quick reference while setting up.

## ☐ Pre-Setup (5 min)
- [ ] Have GitHub account
- [ ] Have Git installed
- [ ] Have all project files ready

## ☐ GitHub Setup (10 min)
- [ ] Create new repository on GitHub
- [ ] Clone repository to computer
- [ ] Copy all files to local repository
- [ ] Create `.github/workflows/` folder structure
- [ ] Add `update-feed.yml` workflow file
- [ ] Commit and push to GitHub

## ☐ Enable Automation (3 min)
- [ ] Go to Actions tab on GitHub
- [ ] Manually trigger workflow to test
- [ ] Verify `research_feed.html` appears
- [ ] Check that workflow succeeded (green checkmark)

## ☐ Enable Hosting (3 min)
- [ ] Go to Settings → Pages
- [ ] Select branch: `main`, folder: `/ (root)`
- [ ] Click Save
- [ ] Wait 1-2 minutes for deployment
- [ ] Copy your live URL

## ☐ Verification (5 min)
- [ ] Visit your live URL
- [ ] Verify all journals show articles
- [ ] Test a DOI link
- [ ] Check mobile view
- [ ] Bookmark the URL

## ☐ Share (2 min)
- [ ] Send URL to colleagues
- [ ] Optional: Create shortened URL
- [ ] Optional: Add to department resources

## ☐ Future Maintenance
- [ ] Check Actions tab weekly for errors
- [ ] Add new journals as needed
- [ ] Update styling if desired

---

## Your URLs (fill in after setup):

**Repository:**
```
https://github.com/YOUR-USERNAME/REPO-NAME
```

**Live Feed:**
```
https://YOUR-USERNAME.github.io/REPO-NAME/research_feed.html
```

**Actions Dashboard:**
```
https://github.com/YOUR-USERNAME/REPO-NAME/actions
```

---

## Time Estimate: ~30 minutes total
Most of this is one-time setup. After that, it runs automatically!
