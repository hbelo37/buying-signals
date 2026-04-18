import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")


KEYWORD_MAP = {
    "growth_expansion": ["expand", "expansion", "launch", "opening", "new office"],
    "tech_stack": ["integration", "platform", "tool", "software"],
    "other": ["partner", "collaborate", "announce"]
}


FUNDING_KEYWORDS = ["raised", "funding", "series", "valuation", "investment"]
HIRING_KEYWORDS = ["hiring", "jobs", "careers", "recruiting", "talent acquisition"]
MAX_NEWS_RESULTS = 10


def _normalize_text(value):
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def _company_aliases(company, domain=None):
    aliases = {_normalize_text(company)}

    compact_name = re.sub(r"[^a-z0-9]", "", company.lower())
    if compact_name:
        aliases.add(compact_name)

    if domain:
        slug = domain.split(".")[0].lower().strip()
        aliases.add(_normalize_text(slug))
        aliases.add(re.sub(r"[^a-z0-9]", "", slug))

    return {alias for alias in aliases if alias}


def _matches_company(article_text, aliases):
    normalized_text = _normalize_text(article_text)
    compact_text = re.sub(r"[^a-z0-9]", "", article_text.lower())

    return any(
        alias in normalized_text or alias in compact_text
        for alias in aliases
    )


def _dedupe(items):
    seen = set()
    result = []

    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)

    return result


def _article_signal(title, snippet):
    snippet = (snippet or "").strip()
    if snippet:
        return f"{title} - {snippet}"
    return title


# ------------------------
# NEWS SIGNALS (SERP)
# ------------------------

def fetch_news(company, domain=None):
    url = "https://serpapi.com/search.json"
    aliases = _company_aliases(company, domain)

    query_terms = [
        f"\"{company}\"",
        "hiring OR jobs OR careers OR recruiting OR talent acquisition OR funding OR raised OR expansion OR launch OR partnership OR integration"
    ]

    if domain:
        query_terms.append(f"\"{domain}\"")

    params = {
        "engine": "google_news",
        "q": " ".join(query_terms),
        "api_key": SERP_API_KEY
    }

    print(f"Calling SerpAPI for: {company}")
    res = requests.get(url, params=params, timeout=20).json()

    news_results = res.get("news_results", [])

    structured = {
        "hiring": [],
        "funding": [],
        "growth_expansion": [],
        "tech_stack": [],
        "other": []
    }

    for n in news_results[:MAX_NEWS_RESULTS]:
        title = (n.get("title") or "").strip()
        snippet = (n.get("snippet") or "").strip()
        source = (n.get("source") or {}).get("name", "")
        article_text = " ".join([title, snippet, source])

        if not title:
            continue

        if not _matches_company(article_text, aliases):
            continue

        signal_text = _article_signal(title, snippet)
        article_lower = article_text.lower()

        if any(k in article_lower for k in HIRING_KEYWORDS):
            structured["hiring"].append(signal_text)
            continue

        if any(k in article_lower for k in FUNDING_KEYWORDS):
            structured["funding"].append(signal_text)
            continue

        matched = False

        for signal_type, keywords in KEYWORD_MAP.items():
            if any(k in article_lower for k in keywords):
                structured[signal_type].append(signal_text)
                matched = True
                break

        if not matched:
            structured["other"].append(signal_text)

    return {
        "hiring": _dedupe(structured["hiring"])[:5],
        "funding": _dedupe(structured["funding"])[:5],
        "growth_expansion": _dedupe(structured["growth_expansion"])[:5],
        "tech_stack": _dedupe(structured["tech_stack"])[:5],
        "other": _dedupe(structured["other"])[:5]
    }


# ------------------------
# HIRING SIGNALS (REAL)
# ------------------------

def fetch_hiring(domain):
    roles = []

    company_slug = domain.split(".")[0]

    # Greenhouse
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
        res = requests.get(url).json()

        for job in res.get("jobs", [])[:15]:
            title = job.get("title", "")
            if any(k in title.lower() for k in ["hr", "recruit", "talent"]):
                roles.append(title)
    except:
        pass

    # Lever
    try:
        url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
        res = requests.get(url).json()

        for job in res[:15]:
            title = job.get("text", "")
            if any(k in title.lower() for k in ["hr", "recruit", "talent"]):
                roles.append(title)
    except:
        pass

    return roles[:5]


# ------------------------
# MAIN SIGNAL AGGREGATOR
# ------------------------

def get_signals(company, domain):
    news_signals = fetch_news(company, domain)

    hiring_roles = fetch_hiring(domain) if domain else []

    structured = {
        "hiring": _dedupe(hiring_roles + news_signals.get("hiring", []))[:5],
        "funding": news_signals.get("funding", []),
        "growth_expansion": news_signals.get("growth_expansion", []),
        "tech_stack": news_signals.get("tech_stack", []),
        "other": news_signals.get("other", [])
    }

    return {
        "structured_signals": structured
    }
