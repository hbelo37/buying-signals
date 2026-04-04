from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze(company, signals, product_context, signal_definitions):
    prompt = f"""
You are a GTM analyst.

Company: {company}

Product:
{product_context["category"]} - {product_context["description"]}

Raw Signals:
{signals["raw_text"]}

-------------------------------------
SIGNAL DEFINITIONS:
{signal_definitions}
-------------------------------------

TASK:

1. Company summary (1 line)

2. Extract signals STRICTLY:

- hiring → ONLY relevant roles
- funding → ONLY real funding
- growth_expansion → new office / geo / product
- tech_stack → tools used
- other → partnerships / GTM signals

STRICT RULES:
- NO assumptions
- NO boolean values
- Only factual statements
- If none → []

-------------------------------------

3. Intent: Hot / Warm / Cold  
4. Confidence (0–1)

5. Explanation:
MAX 1 line based ONLY on signals

6. Outreach:
ONLY if signals exist
Else return []

-------------------------------------

RETURN JSON ONLY
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    output = response.choices[0].message.content

    # 🔥 CLEAN RESPONSE
    try:
        return json.loads(output)
    except:
        return {"raw": output}