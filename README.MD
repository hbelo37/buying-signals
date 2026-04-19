# 🚀 Buying Signal Skill

An open-source **GTM signal detection skill** that works as a local tool, a reusable Python module, and an **MCP-style server** for AI assistants like Claude or ChatGPT Desktop.

Give it a company name or domain and it returns:

* Real-world buying signals (funding, hiring, expansion, product launches, partnerships, tech stack clues)
* Intent classification (`Hot` / `Warm` / `Cold`)
* A short GTM explanation
* Suggested outreach steps

## Why this exists

Most GTM intelligence tools are expensive, closed, or hard to customize. This project is designed to be:

* Open source
* Lightweight
* Easy to modify
* Useful inside a terminal, inside an app, or through MCP-compatible AI tools

Instead of hiding signal logic behind a black box, this repo exposes the logic so you can adapt it to your own product, market, and ICP.

## What it does

The workflow is simple:

1. You pass in a company name or domain
2. The repo collects public signals
3. It filters and groups those signals
4. Groq/LLM logic can summarize the signal pattern
5. The output is a structured GTM response you can use for prospecting

## Example output

```json
{
  "company": "Deel",
  "signals": {
    "hiring": ["Hiring for GTM and RevOps roles"],
    "funding": ["Raised funding"],
    "growth_expansion": ["Expanding into new markets"],
    "tech_stack": ["Uses HubSpot, Segment"],
    "other": ["Announced new product initiative"]
  },
  "intent": "Warm",
  "confidence": 0.7,
  "explanation": "Recent hiring and expansion signals suggest active growth.",
  "outreach_steps": [
    "Reference the expansion or hiring signal",
    "Connect the signal to a business problem",
    "Ask for a short conversation"
  ]
}
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/buying-signal-skill.git
cd buying-signal-skill
pip install -r requirements.txt
```

## Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_key_here
SERPAPI_KEY=your_serpapi_key_here
BUILTWITH_API_KEY=your_builtwith_key_here
```

If you are only using the public signal parts, you can leave unused keys blank.

## Local usage

### Option 1: CLI

Run the command-line version to compare output quickly while you develop:

```bash
python cli.py
```

or, if your project uses a module entrypoint:

```bash
python -m src.engine --company "Deel" --domain "deel.com"
```

### Option 2: Python import

You can also use the signal engine directly in your own code:

```python
from src.signals import get_signals

result = get_signals("Deel", "deel.com")
print(result)
```

## MCP usage

This repo can also run as a **local MCP-style tool server**.

That means AI clients can call it as a tool instead of you manually copying outputs.

### Run locally

```bash
python mcp_server.py
```

When the server starts correctly, it will expose the buying signal skill over stdio for MCP-compatible desktop apps.

### Claude Desktop

Add it as a local MCP server in your Claude desktop config and point it to your project script.

Example shape:

```json
{
  "mcpServers": {
    "buying-signals": {
      "command": "/full/path/to/your/venv/bin/python",
      "args": ["/full/path/to/buying-signal-skill/mcp_server.py"]
    }
  }
}
```

After restarting Claude, the tool becomes available inside chat.

## Signal types

This project currently looks at:

* **Hiring** — relevant open roles, GTM roles, sales roles, RevOps roles
* **Funding** — new funding, rounds, valuation, investment signals
* **Growth / expansion** — new offices, markets, products, launches
* **Tech stack** — tools used by the company
* **Other** — partnerships, announcements, notable public activity

## Limitations

This is intentionally lightweight, so a few things can be imperfect:

* Some public signals may be stale
* Public web coverage can miss company activity
* Results depend on source availability
* Keyword filtering is useful, but not perfect

## Roadmap

* Better hiring detection
* Better tech stack detection
* Signal scoring model
* ICP fit scoring from closed-won accounts
* Batch processing
* More MCP tools for specific workflows
* Pain point detection and account intelligence

## Contributing

Pull requests are welcome.

Good contributions:

* Better signal extraction
* Better scoring logic
* New MCP tools
* Better structured outputs
* Improved documentation

## Why this is useful

This project is meant to become a **reusable GTM skill**.

You can use it:

* in the terminal
* in your own scripts
* inside Claude Desktop
* inside ChatGPT-compatible tool workflows
* as a starting point for your own GTM intelligence stack

## Star the repo

If this helps you build better outbound workflows, give the repo a star so others can find it too.
