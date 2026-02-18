# Quick Start Guide

## Get Started in 2 Steps

### 1. Download the Files
You should have these files:
- `journal_aggregator.py` - The main script
- `README.md` - Full documentation
- `requirements.txt` - Dependencies (currently empty - no external dependencies needed!)

### 2. Generate Your Feed
Open your terminal/command prompt and run:

```bash
python journal_aggregator.py
```

This fetches recent articles (last 90 days) from **26 I/O Psychology journals** including:
- Journal of Applied Psychology
- Personnel Psychology  
- Journal of Business and Psychology
- Journal of Organizational Behavior
- Academy of Management Journal
- ...and 21 more!

Then open the newly generated `research_feed.html` in your browser!

**Note:** First run takes 2-3 minutes as it fetches from all 26 journals.

## What You'll See

The HTML dashboard shows:
- ✨ A beautiful, dark-themed interface
- 📚 Articles organized by journal (with color coding)
- 👥 Authors and publication dates
- 📝 Abstracts (fetched from CrossRef and Semantic Scholar)
- 🏷️ Topic tags for quick scanning
- 🔓 Open access indicators
- 🔗 Direct links to read full articles

## Next Steps

### Deploy to GitHub Pages (Recommended)
For automatic daily updates and online hosting:
1. Follow the `DEPLOYMENT_GUIDE.md` step-by-step
2. Your feed will update automatically every day at 9 AM UTC
3. Share a single URL with colleagues
4. **Setup time:** ~30 minutes, then fully automatic!

### Run Automatically on Your Computer
Set up your computer to run the script daily:
- **Mac/Linux**: Use cron (see README for details)
- **Windows**: Use Task Scheduler (see README for details)

### Share With Colleagues
The HTML file works standalone - just share `research_feed.html`:
- Email it as an attachment
- Upload to Google Drive
- Put it on a shared network drive
- Host on any web server

Or deploy it to GitHub Pages for a shareable link (see `DEPLOYMENT_GUIDE.md`).

### Add More Journals
1. Find the journal's ISSN (search "[journal name] ISSN" on Google)
2. Edit `journal_aggregator.py`
3. Add a new entry to the `JOURNALS` list:
   ```python
   {
       "name": "Journal Name Here",
       "publisher": "Publisher",
       "issn": "1234-5678",
       "color": "#FF6B6B"
   }
   ```

## Troubleshooting

**"Network error"** - Check your internet connection  
**"No articles found"** - Journal may not have published in last 90 days, or verify the ISSN is correct  
**Missing abstracts** - The script tries both CrossRef and Semantic Scholar. Some articles still won't have abstracts - click through to read full articles.  
**Script is slow** - Normal! Fetching 26 journals takes 2-3 minutes. The script includes polite delays between API requests.

## Need Help?

See the full `README.md` for:
- Complete list of all 26 journals
- Detailed customization options
- Changing the 90-day time window
- Adding filters and sorting
- Scheduling automatic updates
- Deployment options
- Complete troubleshooting guide

For GitHub Pages deployment, see `DEPLOYMENT_GUIDE.md` for step-by-step instructions.

---

**Questions?** The README has comprehensive documentation.  
**Want to customize?** The Python script is well-commented and easy to modify.  
**Enjoying the tool?** Share it with colleagues who might find it useful!
