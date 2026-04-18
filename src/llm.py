from groq import Groq
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


DEFAULT_SIGNALS = {
    "hiring": [],
    "funding": [],
    "growth_expansion": [],
    "tech_stack": [],
    "other": []
}


def _extract_json_object(output: str) -> str:
    output = re.sub(r"```json|```", "", output).strip()

    start = output.find("{")
    end = output.rfind("}")

    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in model output")

    return output[start:end + 1]


def _normalize_intent(value):
    intent = str(value or "").strip().lower()

    if intent in {"hot", "warm", "cold", "no_intent"}:
        return intent

    return "cold"


def _normalize_confidence(value):
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.0

    return max(0.0, min(1.0, confidence))


def _normalize_signals(signals):
    signals = signals or {}

    return {
        "hiring": [item for item in signals.get("hiring", []) if item],
        "funding": [item for item in signals.get("funding", []) if item],
        "growth_expansion": [item for item in signals.get("growth_expansion", []) if item],
        "tech_stack": [item for item in signals.get("tech_stack", []) if item],
        "other": [item for item in signals.get("other", []) if item]
    }


def _fallback_response(signals, explanation):
    normalized_signals = _normalize_signals(signals)
    has_signals = any(normalized_signals.values())

    return {
        "signals": normalized_signals,
        "intent": "cold" if has_signals else "no_intent",
        "confidence": 0.25 if has_signals else 0.0,
        "explanation": explanation,
        "outreach_steps": []
    }


def clean_json_output(output: str, source_signals=None):
    try:
        parsed = json.loads(_extract_json_object(output))
        parsed["signals"] = _normalize_signals(parsed.get("signals", DEFAULT_SIGNALS))
        parsed["intent"] = _normalize_intent(parsed.get("intent"))
        parsed["confidence"] = _normalize_confidence(parsed.get("confidence"))

        explanation = str(parsed.get("explanation", "")).strip()
        parsed["explanation"] = explanation or "The provided signals indicate limited buying intent."

        outreach_steps = parsed.get("outreach_steps", [])
        if not isinstance(outreach_steps, list):
            outreach_steps = []
        parsed["outreach_steps"] = [step for step in outreach_steps if isinstance(step, str) and step.strip()]

        return parsed

    except Exception:
        return _fallback_response(
            source_signals or DEFAULT_SIGNALS,
            "The model response could not be parsed into valid analysis JSON."
        )


def analyze(company, signals, product_context, signal_definitions):
    structured_signals = _normalize_signals(signals.get("structured_signals", {}))

    if not any(structured_signals.values()):
        return {
            "signals": structured_signals,
            "intent": "no_intent",
            "confidence": 0.0,
            "explanation": "No relevant buying signals were found in the provided inputs.",
            "outreach_steps": []
        }

    prompt = f"""
You are a GTM analyst scoring real buying signals for outbound prioritization.

Company: {company}

Product:
{product_context["category"]} - {product_context["description"]}

Target Persona:
{product_context["target_persona"]}

Signal Definitions:
{signal_definitions}

Signals (REAL, from web + hiring APIs):
{json.dumps(structured_signals, indent=2)}

-------------------------------------

RULES:

- DO NOT invent signals
- ONLY use provided signals
- Prioritize hiring + funding + expansion
- Remove irrelevant signals
- If a signal is weak or generic, exclude it
- Base intent only on the retained signals
- Use concise business language, not marketing filler
- If there are fewer than 2 strong signals, do not overstate confidence
- Outreach steps must be specific to the retained signals

-------------------------------------

TASK:

1. Keep only relevant signals in the `signals` object
2. Set intent to exactly one of: hot, warm, cold
3. Set confidence to a number from 0.0 to 1.0
4. Write a 1-2 sentence explanation grounded in the retained signals
5. Provide 2-4 outreach steps only when the retained signals justify outreach; otherwise return an empty list

-------------------------------------

RETURN ONLY VALID JSON matching this schema:
{{
  "signals": {{
    "hiring": [],
    "funding": [],
    "growth_expansion": [],
    "tech_stack": [],
    "other": []
  }},
  "intent": "hot",
  "confidence": 0.0,
  "explanation": "",
  "outreach_steps": []
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    raw_output = response.choices[0].message.content

    return clean_json_output(raw_output, structured_signals)
