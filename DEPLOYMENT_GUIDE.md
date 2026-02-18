# GitHub Pages Deployment Guide

Follow these steps to get your journal aggregator running automatically and hosted online.

## Prerequisites
- [ ] GitHub account (free)
- [ ] Git installed on your computer ([download here](https://git-scm.com/downloads))

---

## Part 1: Create GitHub Repository (5 minutes)

### Step 1: Create Repository
1. Go to https://github.com/new
2. Repository name: `io-psych-journal-feed` (or any name you prefer)
3. Description: "Automated aggregator for I/O Psychology journals"
4. **Make it Public** (required for free GitHub Pages)
5. ✅ Check "Add a README file"
6. Click "Create repository"

### Step 2: Clone Repository to Your Computer
Open Terminal (Mac) or Command Prompt (Windows) and run:

```bash
# Navigate to where you want the project
cd ~/Documents  # Or wherever you prefer

# Clone the repository (replace YOUR-USERNAME with your GitHub username)
git clone https://github.com/YOUR-USERNAME/io-psych-journal-feed.git

# Enter the directory
cd io-psych-journal-feed
```

---

## Part 2: Add Your Files (3 minutes)

### Step 3: Copy Your Files
Copy these files into the `io-psych-journal-feed` folder:
- ✅ `journal_aggregator.py`
- ✅ `README.md`
- ✅ `QUICK_START.md`
- ✅ `requirements.txt`

Also copy the workflow file I created:
- ✅ `.github/workflows/update-feed.yml`

Your folder structure should look like:
```
io-psych-journal-feed/
├── .github/
│   └── workflows/
│       └── update-feed.yml
├── journal_aggregator.py
├── README.md
├── QUICK_START.md
└── requirements.txt
```

### Step 4: Push to GitHub
In your terminal, run:

```bash
# Add all files
git add .

# Commit with a message
git commit -m "Initial commit: Add journal aggregator"

# Push to GitHub
git push origin main
```

---

## Part 3: Enable GitHub Actions (2 minutes)

### Step 5: Verify Workflow
1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see "Update Research Feed" workflow
4. Click "Run workflow" → "Run workflow" to test it immediately
5. Wait 30-60 seconds and refresh
6. ✅ Green checkmark = Success!

### Step 6: Check Output
1. Go back to the "Code" tab
2. You should now see `research_feed.html` in your repository
3. Click on it to verify it was generated

---

## Part 4: Enable GitHub Pages (2 minutes)

### Step 7: Configure Pages
1. Go to repository Settings (top right)
2. Scroll down to "Pages" in the left sidebar
3. Under "Source":
   - Branch: `main`
   - Folder: `/ (root)`
4. Click "Save"
5. Wait 1-2 minutes for deployment

### Step 8: Get Your URL
After deployment completes, you'll see:
```
Your site is live at https://YOUR-USERNAME.github.io/io-psych-journal-feed/
```

Your feed will be at:
```
https://YOUR-USERNAME.github.io/io-psych-journal-feed/research_feed.html
```

---

## Part 5: Verification (2 minutes)

### Step 9: Test Everything
- [ ] Visit your URL - does the page load?
- [ ] Check that articles are displaying
- [ ] Click a DOI link - does it work?
- [ ] Check mobile view - does it look good?

### Step 10: Set Up Automatic Updates
**Already done!** The workflow runs:
- ✅ Daily at 9 AM UTC automatically
- ✅ Manually via "Actions" → "Run workflow"
- ✅ Whenever you push changes to the repository

---

## Sharing Your Feed

### Option 1: Share the Direct Link
Send colleagues this URL:
```
https://YOUR-USERNAME.github.io/io-psych-journal-feed/research_feed.html
```

### Option 2: Custom Domain (Optional)
If you own a domain:
1. Settings → Pages → Custom domain
2. Enter your domain (e.g., `research.yourdomain.com`)
3. Follow DNS setup instructions

### Option 3: Shorten the URL
Use bit.ly or another URL shortener for a cleaner link to share.

---

## Maintenance & Updates

### Adding More Journals
1. Edit `journal_aggregator.py` on your computer
2. Add journal to the `JOURNALS` list
3. Commit and push:
   ```bash
   git add journal_aggregator.py
   git commit -m "Add [Journal Name]"
   git push
   ```
4. GitHub Actions will automatically regenerate the feed

### Manual Update
1. Go to Actions tab on GitHub
2. Click "Update Research Feed"
3. Click "Run workflow" → "Run workflow"
4. Feed updates in ~1 minute

### Check Update History
- Actions tab shows all runs
- Click any run to see logs
- Green = success, Red = error (with details)

---

## Troubleshooting

### "Workflow failed"
1. Click on the failed run in Actions
2. Expand the red step to see error message
3. Common issues:
   - Network timeout (will auto-retry next day)
   - CrossRef API down (temporary, rare)

### "Page not found (404)"
1. Verify GitHub Pages is enabled
2. Check that `research_feed.html` exists in repository
3. Wait 2-3 minutes after enabling Pages
4. Try force-refresh (Ctrl+Shift+R or Cmd+Shift+R)

### "Articles not updating"
1. Check Actions tab - is the workflow running?
2. Look at the last successful run time
3. Verify cron schedule (9 AM UTC = adjust for your timezone)

---

## What I Can Help With

### ✅ I Can Help You:
1. Create/modify the workflow file
2. Customize the HTML styling
3. Add more journals to the aggregator
4. Add filtering or sorting features
5. Troubleshoot Python script issues
6. Customize the update schedule
7. Add email notifications (via GitHub Actions)

### ❌ I Cannot Directly Do:
1. Create your GitHub account
2. Run git commands on your computer
3. Access your GitHub repository
4. Click buttons in GitHub's web interface

But I can guide you through all of these steps!

---

## Next Steps After Setup

1. **Test it:** Wait 24 hours and check if it auto-updates
2. **Share it:** Send the link to colleagues
3. **Customize it:** Add more journals or change styling
4. **Monitor it:** Check Actions tab occasionally for errors

---

## Quick Commands Reference

```bash
# Check repository status
git status

# Pull latest changes from GitHub
git pull

# Add and commit changes
git add .
git commit -m "Your message here"
git push

# View commit history
git log --oneline
```

---

**Questions?** Let me know what step you're on and I'll help you through it!
