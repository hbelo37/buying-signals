import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")
print("SERP KEY:", SERP_API_KEY)


KEYWORDS = ["hire", "hiring", "jobs", "fund", "raise", "expansion", "launch", "partner"]


def fetch_news(company):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_news",
        "q": f"{company} hiring OR funding OR expansion OR launch OR partnership",
        "api_key": SERP_API_KEY
    }

    print(f"Calling SerpAPI for: {company}")
    res = requests.get(url, params=params).json()

    news_results = res.get("news_results", [])

    clean_news = []

    for n in news_results[:10]:
        title = n.get("title", "")

        if title and any(k in title.lower() for k in KEYWORDS):
            clean_news.append(title)

    # limit to top 5 clean signals
    return clean_news[:5]


def get_signals(company, domain):
    news = fetch_news(company)

    return {
        "news": news,
        "raw_text": news  # clean input to LLM
    }