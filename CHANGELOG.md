# Changelog

## Version 3.0 - March 2026

### 🚀 Major Features

#### 1. **OpenAlex Integration with CrossRef Fallback**

**NEW: Hybrid API System**
- Primary data source: OpenAlex API (better coverage, more journals)
- Automatic fallback: CrossRef API (reliability backup)
- Semantic Scholar: Abstract enrichment (unchanged)

**Why OpenAlex?**
- Covers all 26 journals (vs. 22 with CrossRef alone)
- Better publisher coverage (Elsevier, Annual Reviews)
- More complete metadata (abstracts, OA status)
- Free and well-documented API

**How It Works:**
```
For each journal:
  1. Try OpenAlex first (if API key available)
  2. If OpenAlex fails or returns 0 → Fall back to CrossRef
  3. If no abstract → Try Semantic Scholar
```

**Result:** All 26 journals now return articles! ✓

---

#### 2. **Abstract Display Improvements**

**NEW: Expand/Collapse Functionality**
- Abstracts initially truncated to ~1 line (~200 chars)
- "Show more" / "Show less" toggle for longer abstracts
- Smooth CSS transitions
- Individual per-article controls

**Benefits:**
- Cleaner interface (less scrolling)
- User controls information density
- Faster scanning of article lists
- Full abstracts available on-demand

---

#### 3. **Enhanced Topic Taxonomy (22 Topics)**

**Comprehensive keyword lists with intentional overlaps:**

##### Individual Level (8 topics)
1. **Selection & Assessment** - 15 keywords
2. **Performance** - 12 keywords
3. **Training & Development** - 15 keywords
4. **Motivation** - 10 keywords
5. **Job Attitudes** - 10 keywords
6. **Individual Differences** - 13 keywords
7. **Health & Well-being** - 15 keywords
8. **Turnover & Retention** - 11 keywords

##### Team/Interpersonal Level (4 topics)
9. **Teams** - 12 keywords
10. **Leadership** - 10 keywords
11. **Conflict** - 8 keywords
12. **Networks** - 16 keywords (+77% from v2.0)

##### Organizational Level (5 topics)
13. **Organizational Culture** - 8 keywords
14. **Organizational Change** - 8 keywords
15. **Job Design** - 9 keywords
16. **Diversity & Inclusion** - 15 keywords
17. **HR Systems & Talent Management** - 9 keywords (with corrected capitalization)

##### Contemporary Issues (3 topics)
18. **Remote Work** - 10 keywords
19. **Artificial Intelligence/Technology** - 22 keywords (+83% from v2.0)
20. **Social Responsibility** - 11 keywords

##### Methods (2 topics)
21. **Measurement & Psychometrics** - 20 keywords (+100% from v2.0)
22. **Research Methods** - 60+ keywords (+500% from v2.0)

---

#### 4. **Research Methods Massive Expansion**

**From 10 → 60+ keywords**

Added comprehensive statistical and advanced methods:

**Statistical Methods:**
- Regression, mediation, moderation
- Common method variance (CMV)
- Statistical power, effect size
- SEM, IRT, PLS, Bayesian

**Causal Inference:**
- Endogeneity, instrumental variables
- Propensity score matching
- Difference-in-differences (DID)
- Regression discontinuity
- Interrupted time series

**Qualitative Methods:**
- Qualitative research, grounded theory
- Ethnography, mixed methods

**Advanced/Computational:**
- Machine learning, NLP, text mining
- Agent-based modeling (ABM)
- Network analysis (SNA)
- Big data analytics
- Computational modeling

**Source:** Organizational Research Methods journal analysis (IF: 9.5)

---

#### 5. **Intentional Keyword Overlaps**

**Strategic overlaps between topics for better coverage:**

| Overlapping Keywords | Topics | Rationale |
|---------------------|--------|-----------|
| SEM, Factor Analysis, IRT, PCA | Research Methods + Measurement & Psychometrics | Used both as techniques AND validation tools |
| Network Analysis, SNA | Research Methods + Networks | Both methodological approach AND content |
| Machine Learning, NLP, Text Mining | Research Methods + AI/Technology | Both research techniques AND workplace tech |

**Benefits:**
- Articles spanning domains get tagged appropriately
- Filter by method OR content
- No information loss with 5-topic limit

---

### ✨ Enhanced Features

#### **Stemming for Word Variations**
Uses NLTK's PorterStemmer to catch all variations:
- "leader" → "leaders", "leadership", "leading"
- "mediate" → "mediation", "mediating", "mediator"

#### **Title Weighting (3x Boost)**
- Title match = 3 points
- Abstract match = 1 point
- Rationale: Title keywords are stronger signals

#### **Phrase Matching**
Handles multi-word terms correctly:
- "work-life balance", "job satisfaction", "organizational commitment"

#### **Fallback Mode**
- If nltk unavailable, falls back to basic keyword matching
- Script always works even without nltk

---

### 🔒 Security & Configuration

#### **API Key Management**
**Priority order:**
1. Environment variable: `OPENALEX_API_KEY`
2. Config file: `config.json`
3. Fallback: CrossRef only (some journals may return 0 articles)

**Setup Options:**

**Option A: Environment Variable (Recommended)**
```bash
export OPENALEX_API_KEY="your-key-here"
```

**Option B: Config File (User-Friendly)**
```bash
cp config.example.json config.json
# Edit config.json with your API key
```

#### **GitHub Safety**
- `.gitignore` protects `config.json`
- `config.example.json` provides template
- No hardcoded keys in code

---

### 🔧 Technical Changes

**New Dependencies:**
- `nltk>=3.8.0` (for stemming)

**New Files:**
- `config.example.json` - API key template
- `.gitignore` - Protects secrets and outputs

**Updated Files:**
- `journal_aggregator.py` - OpenAlex integration, abstract improvements
- `requirements.txt` - Added nltk
- `QUICK_START.md` - Updated setup instructions
- `CHANGELOG.md` - This file

**Removed Files:**
- `ISSUE3_ISSN_FIX.md` - Outdated (alternate ISSN approach abandoned)

---

### 📊 Journal Coverage

**All 26 Journals Working:**

Previously problematic (now working via OpenAlex):
- ✅ Leadership Quarterly (was 0 articles)
- ✅ Journal of Vocational Behavior (was 0 articles)
- ✅ Organizational Behavior and Human Decision Processes (was 0 articles)
- ✅ Annual Review of Organizational Psychology and Organizational Behavior (was 0 articles)

**Coverage:** 26/26 journals (100%) ✓

---

### 🚀 Usage

```bash
# 1. Install dependencies
pip install nltk

# 2. Get OpenAlex API key (free)
# Visit: https://openalex.org/settings/api

# 3. Configure (choose one):
# Option A: Environment variable
export OPENALEX_API_KEY="your-key-here"

# Option B: Config file
cp config.example.json config.json
# Edit config.json with your key

# 4. Run the aggregator
python journal_aggregator.py
```

**First run:** Downloads NLTK data (~5MB) automatically

---

### 📈 Expected Improvements

**Topic Detection:**
- Research Methods: 40% → 90% detection
- Network articles: 70% → 95% detection
- AI/ML articles: 80% → 95% detection
- Measurement articles: 60% → 90% detection

**Coverage:**
- v2.0: 22/26 journals working (85%)
- v3.0: 26/26 journals working (100%)

**User Experience:**
- Cleaner interface (collapsible abstracts)
- More accurate topic tagging
- Complete journal coverage

---

### 🐛 Bug Fixes

- Fixed: HR Systems capitalization (was "Hr Systems", now "HR Systems")
- Fixed: 4 journals returning 0 articles (OpenAlex integration)
- Fixed: Abstract display taking too much space (expand/collapse)

---

### 🔜 Future Enhancements

- [ ] Machine learning-based topic classification
- [ ] Author-provided keyword integration
- [ ] Topic co-occurrence analysis
- [ ] Topic trending over time
- [ ] Export to CSV/JSON
- [ ] Email digest option

---

**Version:** 3.0  
**Release Date:** March 2026  
**Previous Version:** 2.0 (CrossRef only, 18 topics, basic matching)
