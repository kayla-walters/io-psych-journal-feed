# Quick Start Guide - I/O Psychology Journal Aggregator v3.0

## Overview

This tool automatically fetches recent articles from 26 top I/O Psychology journals and generates an interactive HTML dashboard with:
- 90-day article feed
- Smart topic tagging (22 categories)
- Advanced filters (journal, topic, open access)
- Collapsible abstracts
- Clean, modern interface

---

## Setup (5 minutes)

### Step 1: Get OpenAlex API Key (Free, 2 minutes)

1. Visit: **https://openalex.org/settings/api**
2. Sign up or log in (free account)
3. Copy your API key

**Why?** OpenAlex provides access to all 26 journals. Without it, the script falls back to CrossRef which only covers 22 journals.

---

### Step 2: Install Dependencies

```bash
pip install nltk
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

---

### Step 3: Configure API Key

Choose **ONE** of these options:

#### **Option A: Environment Variable** (Recommended for personal use)

**Mac/Linux:**
```bash
export OPENALEX_API_KEY="your-key-here"
```

To make it permanent, add to `~/.zshrc` or `~/.bash_profile`:
```bash
echo 'export OPENALEX_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Windows:**
```cmd
set OPENALEX_API_KEY=your-key-here
```

To make it permanent:
```cmd
setx OPENALEX_API_KEY "your-key-here"
```

#### **Option B: Config File** (Easier for beginners, shared projects)

1. Copy the example config:
   ```bash
   cp config.example.json config.json
   ```

2. Edit `config.json` and replace `"your-key-here"` with your actual key:
   ```json
   {
     "openalex_api_key": "your-actual-key-from-openalex"
   }
   ```

3. **Important:** `config.json` is gitignored - your key stays private!

---

### Step 4: Run the Script

```bash
python journal_aggregator.py
```

**First run:**
- Downloads NLTK data (~5MB) automatically
- Fetches articles from all 26 journals
- Takes ~2 minutes
- Generates `research_feed.html`

**Subsequent runs:**
- NLTK data already downloaded
- Faster execution (~1-2 minutes)

---

## Usage

### Open the Dashboard

```bash
# Mac
open research_feed.html

# Linux
xdg-open research_feed.html

# Windows
start research_feed.html
```

### Features

**Filters:**
- **Journal:** View articles from specific journals
- **Topic:** Filter by 22 I/O psychology topics
- **Search:** Find articles by title keywords
- **Open Access:** Show only freely available articles
- **Show Abstracts:** Toggle abstract visibility

**Sorting:**
- Date (Newest/Oldest First)
- Journal (Alphabetical)
- Title (A-Z)

**Abstracts:**
- Initially collapsed (1 line)
- Click "Show more" to expand individual abstracts
- Or use "Show Abstracts" checkbox to show all

---

## Journals Covered (26)

### Tier 1: Core I/O Psychology
- Journal of Applied Psychology
- Personnel Psychology
- Journal of Business and Psychology
- Journal of Occupational and Organizational Psychology
- Organizational Behavior and Human Decision Processes
- Journal of Organizational Behavior
- Work & Stress
- Human Resource Management
- Journal of Vocational Behavior

### Tier 2: Management & OB
- Academy of Management Journal
- Academy of Management Review
- Administrative Science Quarterly
- Organization Science
- Journal of Management
- Leadership Quarterly
- Organizational Psychology Review
- Annual Review of Organizational Psychology and Organizational Behavior

### Tier 3: Specialized & Applied
- Journal of Occupational Health Psychology
- Journal of Managerial Psychology
- European Journal of Work and Organizational Psychology
- Human Performance
- International Journal of Selection and Assessment
- Group & Organization Management
- Human Resource Development Quarterly
- Industrial and Organizational Psychology
- Journal of Personnel Psychology

---

## Topics (22)

### Individual Level (8)
- Selection & Assessment
- Performance
- Training & Development
- Motivation
- Job Attitudes
- Individual Differences
- Health & Well-being
- Turnover & Retention

### Team Level (4)
- Teams
- Leadership
- Conflict
- Networks

### Organizational Level (5)
- Organizational Culture
- Organizational Change
- Job Design
- Diversity & Inclusion
- HR Systems & Talent Management

### Contemporary (3)
- Remote Work
- Artificial Intelligence/Technology
- Social Responsibility

### Methods (2)
- Measurement & Psychometrics
- Research Methods

---

## Demo Mode

Test the interface without fetching real data:

```bash
python journal_aggregator.py --demo
```

Generates sample data instantly.

---

## Troubleshooting

### "No OpenAlex API key found"

**Solution 1:** Add environment variable
```bash
export OPENALEX_API_KEY="your-key"
```

**Solution 2:** Create config.json
```json
{
  "openalex_api_key": "your-key"
}
```

The script will still work without a key (using CrossRef fallback), but 4 journals may return 0 articles.

---

### "nltk not found" or Import Error

**Solution:**
```bash
pip install nltk
```

If that doesn't work, try:
```bash
pip3 install nltk
```

---

### Some Journals Return 0 Articles

**Likely cause:** No OpenAlex API key

**Check:**
1. Is `OPENALEX_API_KEY` set? (run `echo $OPENALEX_API_KEY`)
2. Does `config.json` exist with valid key?

**Fix:** Follow Step 1 and Step 3 above

---

### Network Errors

**Possible causes:**
- Internet connection issue
- API temporarily down
- Rate limiting (unlikely)

**Fix:**
- Check internet connection
- Wait a few minutes and try again
- APIs are usually very reliable

---

## Advanced Usage

### Custom Article Limit

Edit `journal_aggregator.py`, line ~275:

```python
articles = fetch_feed(journal, max_articles=100)  # Change 100 to desired number
```

### Adjust Date Range

Edit line ~90 (OpenAlex) or ~193 (CrossRef):

```python
ninety_days_ago = dt.now() - timedelta(days=90)  # Change 90 to desired days
```

### Add Custom Topics

Edit `topic_keywords` dictionary in `extract_topics()` function (line ~409):

```python
topic_keywords = {
    'Your Custom Topic': [
        'keyword1', 'keyword2', 'keyword3'
    ],
    # ... existing topics
}
```

---

## Updating

To get the latest version:

```bash
git pull origin main
pip install -r requirements.txt
```

Your `config.json` and API key will be preserved (gitignored).

---

## GitHub Setup

Before pushing to GitHub:

1. **Verify .gitignore exists:**
   ```bash
   cat .gitignore | grep config.json
   ```
   Should show: `config.json`

2. **Check git status:**
   ```bash
   git status
   ```
   `config.json` should NOT appear in the list

3. **Safe to commit:**
   ```bash
   git add journal_aggregator.py requirements.txt .gitignore config.example.json
   git commit -m "Update to v3.0"
   git push
   ```

**Never commit `config.json`** - it contains your API key!

---

## Performance

**Typical execution:**
- Fetching 26 journals: ~2 minutes
- Generating HTML: <1 second
- Total: ~2 minutes

**Data freshness:**
- Last 90 days of articles
- Run weekly or monthly to stay updated

**Output size:**
- HTML file: ~500KB - 2MB (depends on article count)
- Opens instantly in browser

---

## Support

**Issues?**
1. Check this guide's Troubleshooting section
2. Review error messages carefully
3. Verify API key is set correctly

**Want to contribute?**
- Add more journals
- Improve topic keywords
- Enhance UI design
- Submit pull requests welcome!

---

## Version Information

**Current Version:** 3.0 (March 2026)

**What's New in 3.0:**
- ✅ OpenAlex integration (all 26 journals working)
- ✅ Collapsible abstracts (cleaner interface)
- ✅ Expanded Research Methods keywords (+50 terms)
- ✅ Fixed HR capitalization bug
- ✅ Secure API key management

**Previous Version:** 2.0
- 22/26 journals working
- 18 topics
- Basic keyword matching

---

**Happy researching!** 📚🔬

For detailed changes, see [CHANGELOG.md](CHANGELOG.md)
