# 🚀 Buying Signal Skill (MCP-style)

A lightweight, open-source **GTM signal detection engine** that takes a company name or domain and returns:

* Real-world buying signals (funding, hiring, expansion, etc.)
* Intent classification (Hot / Warm / Cold)
* AI-generated GTM explanation
* Suggested outreach steps

---

## 🔥 Why this exists

Most GTM tools:

* Are expensive (ZoomInfo, 6sense, etc.)
* Hide signal logic
* Don’t adapt to your product

This project is:

* ✅ Open source
* ✅ Customizable
* ✅ LLM-powered
* ✅ Built for modern GTM workflows

---

## ⚙️ How it works

```text
Input (company/domain)
        ↓
SerpAPI (news signals)
        ↓
Signal filtering (keywords)
        ↓
LLM analysis (Groq)
        ↓
Structured GTM output
```

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/buying-signal-skill.git
cd buying-signal-skill
pip install -r requirements.txt
```

---

## 🔑 Setup

Create a `.env` file:

```bash
GROQ_API_KEY=your_key
SERPAPI_KEY=your_key
```

---

## ▶️ Usage

```bash
python -m src.engine --company "Deel" --domain "deel.com"
```

---

## 🧪 Example Output

```json
{
  "company": "Deel",
  "signals": {
    "funding": ["Raised $300M in Series E"],
    "growth_expansion": ["Expanding globally"],
    "other": ["Launched new HR product"]
  },
  "intent": "Warm",
  "confidence": 0.7,
  "explanation": "Recent funding and expansion indicate growth",
  "outreach_steps": [
    "Step 1: Reference expansion",
    "Step 2: Position product value",
    "Step 3: Ask for demo"
  ]
}
```

---

## 🧠 Signal Types

* **Hiring** → Relevant open roles
* **Funding** → Capital raised
* **Growth/Expansion** → New markets, offices, products
* **Tech Stack** → Tools used
* **Other** → Partnerships, announcements

---

## 🚧 Current Limitations

* Relies on news signals (no direct hiring scraping yet)
* No CRM enrichment
* Basic keyword filtering

---

## 🚀 Roadmap

* [ ] Hiring signals (Greenhouse / Lever)
* [ ] Tech stack (BuiltWith)
* [ ] Signal scoring engine
* [ ] ICP filtering
* [ ] Batch processing

---

## 🤝 Contributing

PRs welcome. Build your own GTM skills on top of this.

---

## ⭐ If you found this useful

Give it a star — helps others discover it.
