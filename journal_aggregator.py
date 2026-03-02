#!/usr/bin/env python3
"""
Journal Article Aggregator v3.0
Fetches recent articles from I/O Psychology journals using OpenAlex and CrossRef APIs
"""

import urllib.request
import json
import os
import hashlib
from datetime import datetime as dt
from datetime import timedelta
import time

# API Configuration
def get_api_key():
    """Get OpenAlex API key from environment variable or config file"""
    # Priority 1: Environment variable
    key = os.environ.get('OPENALEX_API_KEY')
    if key:
        return key
    
    # Priority 2: Config file
    config_path = 'config.json'
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
                key = config.get('openalex_api_key')
                if key:
                    return key
        except Exception as e:
            print(f"Warning: Could not read config.json: {e}")
    
    # No key found
    return None

OPENALEX_API_KEY = get_api_key()

# Journal configuration with ISSNs
JOURNALS = [
    # Tier 1: Core I/O Psychology Journals
    {"name": "Journal of Applied Psychology", "publisher": "APA", "issn": "0021-9010", "color": "#0066CC"},
    {"name": "Personnel Psychology", "publisher": "Wiley", "issn": "1744-6570", "color": "#006B3D"},
    {"name": "Journal of Business and Psychology", "publisher": "Springer", "issn": "1573-353X", "color": "#FFB81C"},
    {"name": "Journal of Occupational and Organizational Psychology", "publisher": "BPS/Wiley", "issn": "2044-8325", "color": "#8B0000"},
    {"name": "Organizational Behavior and Human Decision Processes", "publisher": "Elsevier", "issn": "0749-5978", "color": "#2E8B57"},
    {"name": "Journal of Organizational Behavior", "publisher": "Wiley", "issn": "1099-1379", "color": "#FF6347"},
    {"name": "Work & Stress", "publisher": "Taylor & Francis", "issn": "1464-5335", "color": "#1E90FF"},
    {"name": "Human Resource Management", "publisher": "Wiley", "issn": "1099-050X", "color": "#FF8C00"},
    {"name": "Journal of Vocational Behavior", "publisher": "Elsevier", "issn": "0001-8791", "color": "#9370DB"},
    
    # Tier 2: Management & OB Journals with Strong I/O Content
    {"name": "Academy of Management Journal", "publisher": "AOM", "issn": "0001-4273", "color": "#DC143C"},
    {"name": "Academy of Management Review", "publisher": "AOM", "issn": "0363-7425", "color": "#00CED1"},
    {"name": "Administrative Science Quarterly", "publisher": "Sage", "issn": "0001-8392", "color": "#FF1493"},
    {"name": "Organization Science", "publisher": "INFORMS", "issn": "1047-7039", "color": "#32CD32"},
    {"name": "Journal of Management", "publisher": "Sage", "issn": "0149-2063", "color": "#BA55D3"},
    {"name": "Leadership Quarterly", "publisher": "Elsevier", "issn": "1048-9843", "color": "#20B2AA"},
    {"name": "Organizational Psychology Review", "publisher": "Sage", "issn": "2041-3866", "color": "#FF4500"},
    {"name": "Annual Review of Organizational Psychology and Organizational Behavior", "publisher": "Annual Reviews", "issn": "2327-0608", "color": "#4B0082"},
    
    # Tier 3: Specialized & Applied I/O Journals
    {"name": "Journal of Occupational Health Psychology", "publisher": "APA", "issn": "1076-8998", "color": "#6A5ACD"},
    {"name": "Journal of Managerial Psychology", "publisher": "Emerald", "issn": "0268-3946", "color": "#008B8B"},
    {"name": "European Journal of Work and Organizational Psychology", "publisher": "Taylor & Francis", "issn": "1359-432X", "color": "#CD5C5C"},
    {"name": "Human Performance", "publisher": "Taylor & Francis", "issn": "0895-9285", "color": "#4682B4"},
    {"name": "International Journal of Selection and Assessment", "publisher": "Wiley", "issn": "0965-075X", "color": "#D2691E"},
    {"name": "Group & Organization Management", "publisher": "Sage", "issn": "1059-6011", "color": "#9932CC"},
    {"name": "Human Resource Development Quarterly", "publisher": "Wiley", "issn": "1044-8004", "color": "#228B22"},
    {"name": "Industrial and Organizational Psychology: Perspectives on Science and Practice", "publisher": "Cambridge", "issn": "1754-9426", "color": "#B8860B"},
    {"name": "Journal of Personnel Psychology", "publisher": "Hogrefe", "issn": "1866-5888", "color": "#5F9EA0"}
]

def fetch_semantic_scholar_abstract(doi):
    """Fetch abstract from Semantic Scholar API if not available from primary source"""
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=abstract"
        headers = {'User-Agent': 'JournalAggregator/3.0 (mailto:researcher@example.com)'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        if 'abstract' in data and data['abstract']:
            return data['abstract']
        return ""
    except Exception:
        return ""

def fetch_openalex(journal, max_articles=100):
    """Fetch recent articles from OpenAlex API for a journal (last 90 days)"""
    try:
        print(f"Fetching {journal['name']} (OpenAlex)...")
        
        ninety_days_ago = dt.now() - timedelta(days=90)
        date_filter = ninety_days_ago.strftime("%Y-%m-%d")
        
        # Build OpenAlex API URL
        base_url = "https://api.openalex.org/works"
        params = f"?filter=primary_location.source.issn:{journal['issn']},from_publication_date:{date_filter}&per-page={max_articles}&sort=publication_date:desc"
        
        if OPENALEX_API_KEY:
            params += f"&api_key={OPENALEX_API_KEY}"
        
        url = base_url + params
        
        headers = {'User-Agent': 'JournalAggregator/3.0 (mailto:researcher@example.com)'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
        
        articles = []
        if 'results' in data:
            for item in data['results']:
                # Parse publication date
                pub_date = None
                date_str = "Date unavailable"
                
                if 'publication_date' in item and item['publication_date']:
                    try:
                        pub_date = dt.strptime(item['publication_date'], "%Y-%m-%d")
                        date_str = pub_date.strftime("%B %d, %Y")
                    except:
                        pass
                
                # Skip if no valid date or outside 90-day window
                if not pub_date or pub_date < ninety_days_ago:
                    continue
                
                # Get authors
                authors = ""
                if 'authorships' in item and item['authorships']:
                    author_list = []
                    for authorship in item['authorships'][:5]:
                        author = authorship.get('author', {})
                        display_name = author.get('display_name', '')
                        if display_name:
                            author_list.append(display_name)
                    
                    if len(item['authorships']) > 5:
                        author_list.append("et al.")
                    authors = ", ".join(author_list)
                
                # Get DOI and link
                doi = item.get('doi', '').replace('https://doi.org/', '') if item.get('doi') else ''
                link = f"https://doi.org/{doi}" if doi else item.get('id', '')
                
                # Get abstract (OpenAlex often has it)
                abstract = ""
                if 'abstract_inverted_index' in item and item['abstract_inverted_index']:
                    # Reconstruct abstract from inverted index
                    inverted_index = item['abstract_inverted_index']
                    words = {}
                    for word, positions in inverted_index.items():
                        for pos in positions:
                            words[pos] = word
                    if words:
                        abstract = ' '.join([words[i] for i in sorted(words.keys())])
                
                # If no abstract from OpenAlex and we have DOI, try Semantic Scholar
                if not abstract and doi:
                    abstract = fetch_semantic_scholar_abstract(doi)
                    if abstract:
                        print(f"    → Found abstract via Semantic Scholar")
                
                # Get title - SKIP if no valid title (likely issue landing page, not article)
                title = item.get('title')
                if not title or not isinstance(title, str) or title.strip() == '':
                    continue  # Skip this record entirely
                
                # Check if open access
                is_open_access = False
                if 'open_access' in item:
                    is_open_access = item['open_access'].get('is_oa', False)
                
                # Extract topics
                topics = extract_topics(title, abstract)
                
                article = {
                    "title": title,
                    "link": link,
                    "authors": authors,
                    "abstract": abstract,
                    "date": pub_date,
                    "date_str": date_str,
                    "journal": journal['name'],
                    "journal_color": journal['color'],
                    "is_open_access": is_open_access,
                    "topics": topics
                }
                articles.append(article)
        
        print(f"  ✓ Found {len(articles)} articles in last 90 days")
        return articles
    
    except urllib.error.URLError as e:
        print(f"  ✗ OpenAlex error for {journal['name']}: {str(e)}")
        return None
    except Exception as e:
        print(f"  ✗ OpenAlex error for {journal['name']}: {str(e)}")
        return None

def fetch_crossref(journal, max_articles=100):
    """Fetch recent articles from CrossRef API for a journal (last 90 days)"""
    try:
        print(f"Fetching {journal['name']} (CrossRef)...")
        
        ninety_days_ago = dt.now() - timedelta(days=90)
        date_filter = ninety_days_ago.strftime("%Y-%m-%d")
        
        # Build CrossRef API URL
        base_url = f"https://api.crossref.org/journals/{journal['issn']}/works"
        params = f"?rows={max_articles}&filter=from-online-pub-date:{date_filter}&sort=published&order=desc"
        url = base_url + params
        
        headers = {'User-Agent': 'JournalAggregator/3.0 (mailto:researcher@example.com)'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
        
        articles = []
        if 'message' in data and 'items' in data['message']:
            for item in data['message']['items']:
                # Parse publication date
                pub_date = None
                date_str = "Date unavailable"
                
                date_parts = None
                if 'published-online' in item:
                    date_parts = item['published-online'].get('date-parts', [[]])[0]
                elif 'published' in item:
                    date_parts = item['published'].get('date-parts', [[]])[0]
                elif 'published-print' in item:
                    date_parts = item['published-print'].get('date-parts', [[]])[0]
                
                if date_parts and len(date_parts) >= 1:
                    year = date_parts[0]
                    month = date_parts[1] if len(date_parts) > 1 else 1
                    day = date_parts[2] if len(date_parts) > 2 else 1
                    pub_date = dt(year, month, day)
                    date_str = pub_date.strftime("%B %d, %Y")
                
                # Skip if no valid date or outside 90-day window
                if not pub_date or pub_date < ninety_days_ago:
                    continue
                
                # Get authors
                authors = ""
                if 'author' in item:
                    author_list = []
                    for author in item['author'][:5]:
                        given = author.get('given', '')
                        family = author.get('family', '')
                        if given and family:
                            author_list.append(f"{given} {family}")
                        elif family:
                            author_list.append(family)
                    
                    if len(item['author']) > 5:
                        author_list.append("et al.")
                    authors = ", ".join(author_list)
                
                # Get DOI
                doi = item.get('DOI', '')
                link = f"https://doi.org/{doi}" if doi else item.get('URL', '')
                
                # Get abstract
                abstract = item.get('abstract', '')
                if not abstract and doi:
                    abstract = fetch_semantic_scholar_abstract(doi)
                    if abstract:
                        print(f"    → Found abstract via Semantic Scholar")
                
                # Get title - SKIP if no valid title (likely issue landing page, not article)
                title = ""
                if 'title' in item and item['title']:
                    title = item['title'][0] if isinstance(item['title'], list) else item['title']
                
                if not title or not isinstance(title, str) or title.strip() == '':
                    continue  # Skip this record entirely
                
                # Check if open access
                is_open_access = False
                if 'link' in item:
                    for link_item in item['link']:
                        if link_item.get('intended-application') == 'text-mining':
                            is_open_access = True
                            break
                if 'license' in item and len(item['license']) > 0:
                    is_open_access = True
                
                # Extract topics
                topics = extract_topics(title, abstract)
                
                article = {
                    "title": title or "No title",
                    "link": link,
                    "authors": authors,
                    "abstract": abstract,
                    "date": pub_date,
                    "date_str": date_str,
                    "journal": journal['name'],
                    "journal_color": journal['color'],
                    "is_open_access": is_open_access,
                    "topics": topics
                }
                articles.append(article)
        
        print(f"  ✓ Found {len(articles)} articles in last 90 days")
        return articles
    
    except urllib.error.URLError as e:
        print(f"  ✗ CrossRef error for {journal['name']}: {str(e)}")
        return []
    except Exception as e:
        print(f"  ✗ CrossRef error for {journal['name']}: {str(e)}")
        return []

def fetch_feed(journal, max_articles=100):
    """
    Hybrid fetch: Try OpenAlex first (better coverage), fall back to CrossRef
    """
    # Try OpenAlex first if API key is available
    if OPENALEX_API_KEY:
        articles = fetch_openalex(journal, max_articles)
        if articles is not None and len(articles) > 0:
            return articles
        
        # OpenAlex failed or returned 0 results, try CrossRef
        print(f"  → Trying CrossRef fallback...")
    
    # Fall back to CrossRef
    return fetch_crossref(journal, max_articles)

def extract_topics(title, abstract):
    """
    Extract key topics from title and abstract using enhanced keyword matching.
    Features: stemming, title weighting (3x), phrase matching
    """
    try:
        import nltk
        from nltk.stem import PorterStemmer
        
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
    except ImportError:
        print("Warning: nltk not available, using basic keyword matching")
        return extract_topics_basic(title, abstract)
    
    # 22-topic taxonomy with comprehensive keywords
    topic_keywords = {
        'Selection & Assessment': [
            'selection', 'select', 'recruit', 'recruitment', 'hiring', 'hire', 
            'assessment', 'assess', 'interview', 'testing', 'test validity',
            'applicant', 'candidate', 'screening', 'personnel selection'
        ],
        'Performance': [
            'performance', 'perform', 'productivity', 'productive', 
            'performance appraisal', 'performance management', 'evaluation',
            'task performance', 'contextual performance', 'job performance',
            'effectiveness', 'efficient'
        ],
        'Training & Development': [
            'training', 'train', 'development', 'develop', 'learning', 'learn',
            'skill development', 'career development', 'onboarding', 'orientation',
            'socialization', 'upskilling', 'reskilling', 'coaching', 'mentoring'
        ],
        'Motivation': [
            'motivation', 'motivate', 'motivated', 'goal setting', 'goal',
            'self-determination', 'incentive', 'reward', 'intrinsic', 'extrinsic'
        ],
        'Job Attitudes': [
            'job satisfaction', 'satisfaction', 'organizational commitment', 
            'commitment', 'affective commitment', 'engagement', 'engaged',
            'job involvement', 'psychological contract', 'attitudes'
        ],
        'Individual Differences': [
            'personality', 'individual differences', 'cognitive ability', 'intelligence',
            'big five', 'traits', 'conscientiousness', 'extraversion', 'openness',
            'agreeableness', 'neuroticism', 'ability', 'aptitude'
        ],
        'Health & Well-being': [
            'well-being', 'wellbeing', 'wellness', 'health', 'mental health',
            'stress', 'stressor', 'strain', 'burnout', 'exhaustion',
            'work-life', 'work-family', 'balance', 'recovery', 'safety', 'injury'
        ],
        'Turnover & Retention': [
            'turnover', 'retention', 'attrition', 'quit', 'quitting', 'leaving',
            'voluntary turnover', 'withdrawal', 'exit', 'stay', 'retain'
        ],
        'Teams': [
            'team', 'teams', 'teamwork', 'group', 'collaboration', 'collaborative',
            'coordination', 'team performance', 'team effectiveness', 'team processes',
            'virtual team', 'multiteam', 'crew'
        ],
        'Leadership': [
            'leadership', 'leader', 'leading', 'supervisor', 'supervisory',
            'transformational leadership', 'servant leadership', 'authentic leadership',
            'ethical leadership', 'abusive supervision', 'leader-member exchange', 'LMX'
        ],
        'Conflict': [
            'conflict', 'disagreement', 'dispute', 'interpersonal conflict',
            'task conflict', 'relationship conflict', 'negotiation', 'bargaining'
        ],
        'Networks': [
            'network', 'social network', 'tie', 'relationship', 'connections',
            'social capital', 'centrality', 'brokerage', 'networking',
            'network analysis', 'social network analysis', 'SNA',
            'ego network', 'whole network', 'network structure',
            'betweenness', 'closeness', 'degree centrality',
            'network density', 'structural holes'
        ],
        'Organizational Culture': [
            'organizational culture', 'culture', 'cultural', 'climate', 
            'organizational climate', 'safety climate', 'values', 'norms'
        ],
        'Organizational Change': [
            'change', 'organizational change', 'transformation', 'reorganization',
            'change management', 'organization development', 'OD', 'intervention'
        ],
        'Job Design': [
            'job design', 'work design', 'task design', 'job characteristics',
            'job crafting', 'autonomy', 'skill variety', 'task significance',
            'job redesign', 'enrichment'
        ],
        'Diversity & Inclusion': [
            'diversity', 'diverse', 'inclusion', 'inclusive', 'equity', 'DEI',
            'bias', 'discrimination', 'prejudice', 'stereotype', 'gender', 
            'race', 'ethnicity', 'belonging', 'microaggression', 'fairness'
        ],
        'HR Systems & Talent Management': [
            'human resource', 'HR', 'talent management', 'succession planning',
            'workforce planning', 'HRIS', 'compensation', 'benefits', 'pay'
        ],
        'Remote Work': [
            'remote work', 'remote', 'telework', 'telecommuting', 'work from home',
            'WFH', 'hybrid work', 'virtual work', 'distributed work', 'flexible work'
        ],
        'Artificial Intelligence/Technology': [
            'artificial intelligence', 'AI', 'machine learning', 'algorithm',
            'algorithmic', 'automation', 'technology', 'digital', 'analytics',
            'big data', 'predictive', 'chatbot', 'robot',
            'natural language processing', 'NLP', 'text mining', 'text analysis',
            'computational modeling', 'deep learning', 'neural network',
            'supervised learning', 'unsupervised learning',
            'data mining', 'predictive analytics', 'sentiment analysis'
        ],
        'Social Responsibility': [
            'sustainability', 'sustainable', 'corporate social responsibility', 'CSR',
            'ESG', 'environmental', 'green', 'climate', 'social impact', 'ethics', 'ethical'
        ],
        'Measurement & Psychometrics': [
            'measurement', 'psychometric', 'scale development', 'validation', 'validate',
            'reliability', 'validity', 'factor analysis', 'construct validity',
            'measurement invariance',
            'structural equation modeling', 'SEM', 
            'confirmatory factor analysis', 'CFA', 'exploratory factor analysis', 'EFA',
            'item response theory', 'IRT',
            'principal component analysis', 'PCA',
            'Rasch model', 'test theory', 'classical test theory'
        ],
        'Research Methods': [
            'meta-analysis', 'meta analysis', 'systematic review', 'methodology',
            'multilevel', 'hierarchical', 'longitudinal', 'experience sampling', 'diary study',
            'experimental design', 'quasi-experimental', 'research design',
            'structural equation modeling', 'SEM', 'regression', 'linear regression',
            'mediation', 'moderation', 'moderator', 'mediator',
            'common method bias', 'common-method variance', 'CMV',
            'item response theory', 'IRT', 
            'statistics', 'statistical', 'statistical power', 'power analysis',
            'qualitative', 'qualitative research', 'grounded theory', 'ethnography',
            'mixed methods', 'data analysis', 'analysis',
            'sampling', 'sample size', 'effect size',
            'Bayesian', 'Monte Carlo', 'simulation',
            'causal inference', 'endogeneity', 'instrumental variable',
            'random effects', 'fixed effects', 'panel data',
            'partial least squares', 'PLS',
            'computational modeling', 'agent-based modeling', 'ABM',
            'network analysis', 'social network analysis', 'SNA',
            'text mining', 'natural language processing', 'NLP',
            'machine learning', 'big data', 'analytics',
            'propensity score', 'matching', 'difference-in-differences', 'DID',
            'interrupted time series', 'regression discontinuity',
            'factor analysis', 'exploratory factor analysis', 'confirmatory factor analysis',
            'principal component', 'PCA'
        ]
    }
    
    stemmer = PorterStemmer()
    
    # Handle None values safely
    title_lower = (title or '').lower()
    abstract_lower = (abstract or '').lower()
    
    # Calculate topic scores
    topic_scores = {}
    
    for topic, keywords in topic_keywords.items():
        score = 0
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Check for exact phrase match (for multi-word terms)
            if ' ' in keyword_lower:
                if keyword_lower in title_lower:
                    score += 3
                if keyword_lower in abstract_lower:
                    score += 1
            else:
                # For single words, use stemming
                keyword_stem = stemmer.stem(keyword_lower)
                title_words = [stemmer.stem(word.strip('.,!?;:()[]{}')) for word in title_lower.split()]
                abstract_words = [stemmer.stem(word.strip('.,!?;:()[]{}')) for word in abstract_lower.split()]
                
                if keyword_stem in title_words:
                    score += 3
                if keyword_stem in abstract_words:
                    score += 1
        
        if score > 0:
            topic_scores[topic] = score
    
    # Return top 5 topics by score
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
    return [topic for topic, score in sorted_topics[:5]]

def extract_topics_basic(title, abstract):
    """Fallback basic keyword matching if nltk not available"""
    topic_keywords = {
        'Selection & Assessment': ['selection', 'recruitment', 'hiring', 'assessment', 'interview'],
        'Performance': ['performance', 'productivity', 'effectiveness'],
        'Training & Development': ['training', 'development', 'learning', 'coaching'],
        'Motivation': ['motivation', 'engagement', 'goal setting'],
        'Job Attitudes': ['satisfaction', 'commitment', 'engagement', 'attitudes'],
        'Individual Differences': ['personality', 'individual differences', 'ability'],
        'Health & Well-being': ['well-being', 'wellbeing', 'health', 'stress', 'burnout'],
        'Turnover & Retention': ['turnover', 'retention', 'attrition'],
        'Teams': ['team', 'teamwork', 'collaboration', 'group'],
        'Leadership': ['leadership', 'leader', 'supervisor'],
        'Conflict': ['conflict', 'disagreement', 'dispute'],
        'Networks': ['network', 'social network', 'network analysis', 'SNA'],
        'Organizational Culture': ['culture', 'climate', 'values'],
        'Organizational Change': ['change', 'transformation', 'organization development'],
        'Job Design': ['job design', 'work design', 'autonomy'],
        'Diversity & Inclusion': ['diversity', 'inclusion', 'bias', 'discrimination'],
        'HR Systems & Talent Management': ['human resource', 'HR', 'talent management'],
        'Remote Work': ['remote work', 'telework', 'hybrid work'],
        'Artificial Intelligence/Technology': ['artificial intelligence', 'AI', 'technology', 'automation', 'machine learning', 'NLP', 'text mining'],
        'Social Responsibility': ['sustainability', 'CSR', 'ethics'],
        'Measurement & Psychometrics': ['measurement', 'validation', 'psychometric', 'SEM', 'factor analysis', 'IRT'],
        'Research Methods': ['meta-analysis', 'systematic review', 'methodology', 'multilevel', 'SEM', 'regression', 'mediation', 'statistics', 'qualitative', 'network analysis', 'machine learning', 'factor analysis']
    }
    
    text = (title + ' ' + abstract).lower()
    found_topics = []
    
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in text:
                found_topics.append(topic)
                break
    
    return found_topics[:5]

def format_topic_name(topic):
    """
    Format topic name preserving special capitalizations (HR)
    """
    # Special case for HR Systems
    if topic == 'HR Systems & Talent Management':
        return 'HR Systems & Talent Management'
    # Use title case for others
    return topic.title()

def generate_html(journal_data, output_file="research_feed.html"):
    """Generate HTML dashboard from journal data with light theme and filters"""
    
    # Combine and sort all articles chronologically
    all_articles = []
    for journal in journal_data:
        all_articles.extend(journal['articles'])
    
    all_articles.sort(key=lambda x: x['date'] if x['date'] else dt.min, reverse=True)
    
    # Split articles into THIS WEEK and LAST 90 DAYS
    now = dt.now()
    week_ago = now - timedelta(days=7)
    
    this_week = [a for a in all_articles if a['date'] and a['date'] >= week_ago]
    last_90_days = [a for a in all_articles if a['date'] and a['date'] < week_ago]
    
    # Get unique journals and topics for filters
    journals_list = list(set([a['journal'] for a in all_articles]))
    all_topics = set()
    for article in all_articles:
        all_topics.update(article['topics'])
    topics_list = sorted(list(all_topics))
    
    total_articles = len(all_articles)
    last_updated = dt.now().strftime("%B %d, %Y")
    
    footer_journals = sorted([j['name'] for j in JOURNALS])
    footer_text = " | ".join(footer_journals)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>I/O Psychology Research Briefing</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f7fa;
            color: #1a1a1a;
            line-height: 1.6;
            min-height: 100vh;
            padding: 2rem 1rem;
        }}
        
        .header-card {{
            max-width: 1200px;
            margin: 0 auto 2rem auto;
            background: white;
            padding: 2rem 1.5rem 1.5rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            text-align: center;
        }}
        
        .header-card h1 {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #003366;
            margin-bottom: 0.4rem;
            letter-spacing: -0.02em;
        }}
        
        .header-card .tagline {{
            font-size: 0.9rem;
            color: #6c757d;
            font-weight: 400;
            margin-bottom: 1.25rem;
        }}
        
        .header-meta {{
            display: flex;
            gap: 2rem;
            justify-content: center;
            font-size: 0.8125rem;
            color: #6c757d;
            flex-wrap: wrap;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}
        
        .filters {{
            background: white;
            padding: 1.25rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .filter-row {{
            display: flex;
            gap: 0.875rem;
            align-items: flex-end;
            margin-bottom: 0.875rem;
            flex-wrap: wrap;
        }}
        
        .filter-row:last-child {{
            margin-bottom: 0;
        }}
        
        .filter-group {{
            flex: 1;
            min-width: 160px;
        }}
        
        .filter-group.search {{
            flex: 2;
            min-width: 220px;
        }}
        
        .filter-label {{
            display: block;
            font-size: 0.8125rem;
            font-weight: 600;
            color: #495057;
            margin-bottom: 0.4rem;
        }}
        
        select, input[type="text"] {{
            width: 100%;
            padding: 0.4rem 0.65rem;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 0.8125rem;
            font-family: 'Inter', sans-serif;
            background: white;
        }}
        
        select:focus, input[type="text"]:focus {{
            outline: none;
            border-color: #003366;
            box-shadow: 0 0 0 3px rgba(0, 51, 102, 0.1);
        }}
        
        .checkbox-group {{
            display: flex;
            align-items: center;
            padding-top: 1.5rem;
        }}
        
        .checkbox-group input[type="checkbox"] {{
            width: auto;
            margin-right: 0.4rem;
            cursor: pointer;
        }}
        
        .checkbox-group label {{
            font-size: 0.8125rem;
            color: #495057;
            cursor: pointer;
            user-select: none;
        }}
        
        .article-count {{
            text-align: center;
            padding: 0.75rem;
            background: white;
            border-radius: 8px;
            margin-bottom: 1.25rem;
            font-size: 0.8125rem;
            color: #6c757d;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        
        .section-header {{
            font-size: 0.875rem;
            font-weight: 700;
            color: #003366;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e1e8ed;
        }}
        
        .feed {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        
        .article {{
            background: white;
            padding: 1rem;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-left: 3px solid #003366;
            transition: box-shadow 0.2s ease, transform 0.2s ease;
        }}
        
        .article:hover {{
            box-shadow: 0 3px 8px rgba(0,0,0,0.15);
            transform: translateY(-1px);
        }}
        
        .article-header {{
            display: flex;
            align-items: flex-start;
            gap: 0.6rem;
            margin-bottom: 0.6rem;
        }}
        
        .article-title {{
            flex: 1;
            font-size: 0.9375rem;
            font-weight: 600;
            line-height: 1.4;
        }}
        
        .article-title a {{
            color: #1a1a1a;
            text-decoration: none;
        }}
        
        .article-title a:hover {{
            color: #003366;
        }}
        
        .open-access {{
            flex-shrink: 0;
            width: 18px;
            height: 18px;
            background: #28a745;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 11px;
            font-weight: bold;
        }}
        
        .article-meta {{
            display: flex;
            gap: 0.75rem;
            margin-bottom: 0.6rem;
            font-size: 0.8125rem;
            color: #6c757d;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .journal-badge {{
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 10px;
            font-size: 0.6875rem;
            font-weight: 600;
            color: white;
        }}
        
        .authors {{
            font-style: italic;
        }}
        
        .date {{
            color: #495057;
        }}
        
        .topics {{
            display: flex;
            gap: 0.4rem;
            margin-bottom: 0.6rem;
            flex-wrap: wrap;
        }}
        
        .topic-tag {{
            display: inline-block;
            padding: 0.2rem 0.4rem;
            background: #e7f3ff;
            color: #003366;
            border-radius: 3px;
            font-size: 0.6875rem;
            font-weight: 500;
        }}
        
        .abstract {{
            color: #495057;
            font-size: 0.8125rem;
            line-height: 1.5;
            margin-bottom: 0.6rem;
        }}
        
        .abstract.truncated {{
            max-height: 3em;
            overflow: hidden;
            position: relative;
        }}
        
        .abstract.truncated::after {{
            content: '...';
            position: absolute;
            bottom: 0;
            right: 0;
            padding-left: 2rem;
            background: linear-gradient(to right, transparent, white 50%);
        }}
        
        .abstract.expanded {{
            max-height: none;
        }}
        
        .abstract.hidden {{
            display: none;
        }}
        
        .no-abstract {{
            color: #adb5bd;
            font-style: italic;
            font-size: 0.8125rem;
        }}
        
        .no-abstract.hidden {{
            display: none;
        }}
        
        .abstract-toggle {{
            display: inline-block;
            color: #003366;
            text-decoration: none;
            font-size: 0.8125rem;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 0.6rem;
        }}
        
        .abstract-toggle:hover {{
            text-decoration: underline;
        }}
        
        .read-more {{
            display: inline-block;
            color: #003366;
            text-decoration: none;
            font-size: 0.8125rem;
            font-weight: 600;
        }}
        
        .read-more:hover {{
            text-decoration: underline;
        }}
        
        .no-results {{
            text-align: center;
            padding: 2.5rem;
            background: white;
            border-radius: 8px;
            color: #6c757d;
            font-style: italic;
        }}
        
        .footer {{
            max-width: 1200px;
            margin: 3rem auto 2rem auto;
            padding: 2rem 1rem 1rem 1rem;
            border-top: 1px solid #e1e8ed;
            text-align: center;
        }}
        
        .footer-title {{
            font-size: 0.75rem;
            font-weight: 600;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.75rem;
        }}
        
        .footer-journals {{
            font-size: 0.6875rem;
            color: #8b949e;
            line-height: 1.6;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem 0.5rem;
            }}
            
            .header-card {{
                padding: 1.5rem 1rem;
            }}
            
            .header-card h1 {{
                font-size: 1.5rem;
            }}
            
            .header-card .tagline {{
                font-size: 0.875rem;
            }}
            
            .filter-row {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .filter-group,
            .filter-group.search {{
                width: 100%;
                min-width: unset;
            }}
            
            .checkbox-group {{
                padding-top: 0;
                margin-top: 0.5rem;
            }}
            
            .article-meta {{
                flex-direction: column;
                gap: 0.25rem;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="header-card">
        <h1>I/O Psychology Research Briefing</h1>
        <div class="tagline">Your 90-day snapshot of what's new in the field</div>
        <div class="header-meta">
            <span>📊 {total_articles} articles</span>
            <span>🕐 Updated: {last_updated}</span>
        </div>
    </div>
    
    <div class="container">
        <div class="filters">
            <div class="filter-row">
                <div class="filter-group">
                    <label class="filter-label" for="journal-filter">Filter by Journal</label>
                    <select id="journal-filter" onchange="filterArticles()">
                        <option value="all">All Journals</option>
"""
    
    for journal in sorted(journals_list):
        html += f"""                        <option value="{journal}">{journal}</option>
"""
    
    html += """                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label" for="topic-filter">Filter by Topic</label>
                    <select id="topic-filter" onchange="filterArticles()">
                        <option value="all">All Topics</option>
"""
    
    for topic in topics_list:
        html += f"""                        <option value="{topic}">{format_topic_name(topic)}</option>
"""
    
    html += """                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label" for="sort-by">Sort by</label>
                    <select id="sort-by" onchange="sortArticles()">
                        <option value="date-newest">Date (Newest First)</option>
                        <option value="date-oldest">Date (Oldest First)</option>
                        <option value="journal">Journal</option>
                        <option value="title">Title (A-Z)</option>
                    </select>
                </div>
            </div>
            <div class="filter-row">
                <div class="filter-group search">
                    <label class="filter-label" for="search">Search</label>
                    <input type="text" id="search" placeholder="Search titles..." oninput="filterArticles()">
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="oa-only" onchange="filterArticles()">
                    <label for="oa-only">Open Access Only</label>
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="expand-abstracts" onchange="toggleAbstracts()">
                    <label for="expand-abstracts">Expand Abstracts</label>
                </div>
            </div>
        </div>
        
        <div class="article-count" id="article-count">
            Showing {total_articles} articles
        </div>
        
        <div id="feed-container">
"""
    
    if this_week:
        html += """            <div class="section-header">This Week</div>
            <div class="feed" data-section="this-week">
"""
        for article in this_week:
            html += generate_article_html(article)
        html += """            </div>
"""
    
    if last_90_days:
        html += """            <div class="section-header">Last 90 Days</div>
            <div class="feed" data-section="last-90-days">
"""
        for article in last_90_days:
            html += generate_article_html(article)
        html += """            </div>
"""
    
    html += """        </div>
        
        <div class="no-results" id="no-results" style="display: none;">
            No articles match your current filters.
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-title">Sources</div>
        <div class="footer-journals">""" + footer_text + """</div>
    </div>
    
    <script>
        function toggleAbstractExpand(articleId) {
            const abstract = document.getElementById('abstract-' + articleId);
            const toggle = document.getElementById('toggle-' + articleId);
            
            if (abstract.classList.contains('truncated')) {
                abstract.classList.remove('truncated');
                abstract.classList.add('expanded');
                toggle.textContent = 'Show less';
            } else {
                abstract.classList.remove('expanded');
                abstract.classList.add('truncated');
                toggle.textContent = 'Show more';
            }
        }
        
        function filterArticles() {
            const journalFilter = document.getElementById('journal-filter').value;
            const topicFilter = document.getElementById('topic-filter').value;
            const searchQuery = document.getElementById('search').value.toLowerCase();
            const oaOnly = document.getElementById('oa-only').checked;
            
            const articles = document.querySelectorAll('.article');
            const sections = document.querySelectorAll('[data-section]');
            const articleCount = document.getElementById('article-count');
            const noResults = document.getElementById('no-results');
            const feedContainer = document.getElementById('feed-container');
            
            let visibleCount = 0;
            
            articles.forEach(article => {
                const journal = article.getAttribute('data-journal');
                const topics = article.getAttribute('data-topics');
                const title = article.getAttribute('data-title');
                const isOA = article.getAttribute('data-oa') === 'true';
                
                let showArticle = true;
                
                if (journalFilter !== 'all' && journal !== journalFilter) {
                    showArticle = false;
                }
                
                if (topicFilter !== 'all') {
                    const topicList = topics.split('|');
                    if (!topicList.includes(topicFilter)) {
                        showArticle = false;
                    }
                }
                
                if (searchQuery && !title.includes(searchQuery)) {
                    showArticle = false;
                }
                
                if (oaOnly && !isOA) {
                    showArticle = false;
                }
                
                if (showArticle) {
                    article.style.display = 'block';
                    visibleCount++;
                } else {
                    article.style.display = 'none';
                }
            });
            
            sections.forEach(section => {
                const visibleInSection = Array.from(section.querySelectorAll('.article'))
                    .filter(a => a.style.display !== 'none').length;
                const sectionHeader = section.previousElementSibling;
                if (visibleInSection === 0) {
                    section.style.display = 'none';
                    if (sectionHeader && sectionHeader.classList.contains('section-header')) {
                        sectionHeader.style.display = 'none';
                    }
                } else {
                    section.style.display = 'flex';
                    if (sectionHeader && sectionHeader.classList.contains('section-header')) {
                        sectionHeader.style.display = 'block';
                    }
                }
            });
            
            const articleWord = visibleCount !== 1 ? 'articles' : 'article';
            articleCount.textContent = 'Showing ' + visibleCount + ' ' + articleWord;
            
            if (visibleCount === 0) {
                feedContainer.style.display = 'none';
                noResults.style.display = 'block';
            } else {
                feedContainer.style.display = 'block';
                noResults.style.display = 'none';
            }
        }
        
        function sortArticles() {
            const sortBy = document.getElementById('sort-by').value;
            const sections = document.querySelectorAll('[data-section]');
            
            sections.forEach(feed => {
                const articles = Array.from(feed.querySelectorAll('.article'));
                
                articles.sort((a, b) => {
                    if (sortBy === 'date-newest') {
                        return parseFloat(b.getAttribute('data-date')) - parseFloat(a.getAttribute('data-date'));
                    } else if (sortBy === 'date-oldest') {
                        return parseFloat(a.getAttribute('data-date')) - parseFloat(b.getAttribute('data-date'));
                    } else if (sortBy === 'journal') {
                        return a.getAttribute('data-journal').localeCompare(b.getAttribute('data-journal'));
                    } else if (sortBy === 'title') {
                        return a.getAttribute('data-title').localeCompare(b.getAttribute('data-title'));
                    }
                    return 0;
                });
                
                articles.forEach(article => feed.appendChild(article));
            });
        }
        
        function toggleAbstracts() {
            const expandAbstracts = document.getElementById('expand-abstracts').checked;
            const abstracts = document.querySelectorAll('.abstract');
            
            abstracts.forEach(abstract => {
                if (expandAbstracts) {
                    abstract.classList.remove('truncated');
                    abstract.classList.add('expanded');
                } else {
                    abstract.classList.remove('expanded');
                    abstract.classList.add('truncated');
                }
            });
            
            // Update all toggle buttons
            const toggles = document.querySelectorAll('.abstract-toggle');
            toggles.forEach(toggle => {
                if (expandAbstracts) {
                    toggle.textContent = 'Show less';
                } else {
                    toggle.textContent = 'Show more';
                }
            });
        }
        
        // Abstracts start visible but truncated (no initialization needed)
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✓ HTML generated: {output_file}")
    return output_file

def generate_article_html(article):
    """Helper function to generate HTML for a single article"""
    # Generate unique ID for this article
    article_id = hashlib.md5(article['title'].encode()).hexdigest()[:8]
    
    journal_color = article.get('journal_color', '#003366')
    
    # Handle abstract
    abstract = article['abstract']
    show_abstract = True
    has_long_abstract = len(abstract) > 200
    
    if not abstract:
        show_abstract = False
    
    # Build topics string (use pipe delimiter to avoid breaking multi-word topics)
    topics_str = '|'.join(article['topics'])
    oa_attr = "true" if article['is_open_access'] else "false"
    
    html = f"""
            <article class="article" data-journal="{article['journal']}" data-topics="{topics_str}" data-title="{article['title'].lower()}" data-oa="{oa_attr}" data-date="{article['date'].timestamp() if article['date'] else 0}">
                <div class="article-header">
                    <div class="article-title">
                        <a href="{article['link']}" target="_blank">{article['title']}</a>
                    </div>
"""
    
    if article['is_open_access']:
        html += """                    <div class="open-access" title="Open Access">🔓</div>
"""
    
    html += """                </div>
                <div class="article-meta">
"""
    
    html += f"""                    <span class="journal-badge" style="background-color: {journal_color};">{article['journal']}</span>
"""
    
    if article['authors']:
        html += f"""                    <span class="authors">{article['authors']}</span>
"""
    
    html += f"""                    <span class="date">{article['date_str']}</span>
                </div>
"""
    
    if article['topics']:
        html += """                <div class="topics">
"""
        for topic in article['topics']:
            html += f"""                    <span class="topic-tag">{format_topic_name(topic)}</span>
"""
        html += """                </div>
"""
    
    if show_abstract:
        truncated_class = 'truncated' if has_long_abstract else ''
        html += f"""                <div id="abstract-{article_id}" class="abstract {truncated_class}">{abstract}</div>
"""
        if has_long_abstract:
            html += f"""                <span id="toggle-{article_id}" class="abstract-toggle" onclick="toggleAbstractExpand('{article_id}')">Show more</span>
"""
    else:
        html += """                <div class="no-abstract">Abstract not available</div>
"""
    
    html += f"""                <a href="{article['link']}" target="_blank" class="read-more">Read full article →</a>
            </article>
"""
    
    return html

def main():
    """Main entry point"""
    import sys
    
    demo_mode = '--demo' in sys.argv
    
    print("=" * 60)
    print("I/O PSYCHOLOGY JOURNAL AGGREGATOR v3.0")
    print("=" * 60)
    print()
    
    # Check for API key
    if not OPENALEX_API_KEY:
        print("⚠️  No OpenAlex API key found")
        print("    The script will use CrossRef as fallback, but some journals may return 0 articles.")
        print("    Get a free API key at: https://openalex.org/settings/api")
        print("    Then set it as:")
        print("    - Environment variable: export OPENALEX_API_KEY='your-key'")
        print("    - Or create config.json with: {\"openalex_api_key\": \"your-key\"}")
        print()
    else:
        print("✓ OpenAlex API key found")
        print()
    
    if demo_mode:
        print("Running in DEMO mode with sample data...")
        print()
        journal_data = get_demo_data()
    else:
        journal_data = []
        for journal in JOURNALS:
            articles = fetch_feed(journal)
            journal_data.append({
                'name': journal['name'],
                'color': journal['color'],
                'articles': articles
            })
            time.sleep(1)
    
    print()
    generate_html(journal_data)
    
    print()
    print("=" * 60)
    print("Done! Open the HTML file in your browser to view.")
    if demo_mode:
        print("(This was demo data. Remove --demo flag to fetch real data)")
    print("=" * 60)

def get_demo_data():
    """Generate sample data for demonstration"""
    return [
        {
            'name': 'Journal of Applied Psychology',
            'color': '#0066CC',
            'articles': [
                {
                    'title': 'The Role of Psychological Safety in Diverse Teams: A Meta-Analysis',
                    'link': 'https://doi.org/10.1037/apl0001234',
                    'authors': 'Sarah Johnson, Michael Chen, Patricia Rodriguez',
                    'abstract': 'This meta-analysis examines the relationship between psychological safety and team performance across diverse organizational contexts. Drawing on 156 studies (N = 42,891 teams), we found that psychological safety significantly predicts team learning behaviors (ρ = .52) and team performance (ρ = .38). The relationship was stronger in knowledge-intensive industries and teams with high task interdependence.',
                    'date': dt(2025, 1, 15),
                    'date_str': 'January 15, 2025',
                    'journal': 'Journal of Applied Psychology',
                    'journal_color': '#0066CC',
                    'is_open_access': True,
                    'topics': ['Teams', 'Diversity & Inclusion', 'Research Methods', 'Performance']
                }
            ]
        }
    ]

if __name__ == "__main__":
    main()
