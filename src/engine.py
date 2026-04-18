import argparse
import json

from src.signals import get_signals
from src.llm import analyze
from src.config import PRODUCT_CONTEXT, SIGNAL_DEFINITIONS


def run(company, domain):
    signals = get_signals(company, domain)

    analysis = analyze(
        company,
        signals,
        PRODUCT_CONTEXT,
        SIGNAL_DEFINITIONS
    )

    # remove outreach if no signals
    if not any(analysis.get("signals", {}).values()):
        analysis["outreach_steps"] = []

    return {
        "company": company,
        "signals": analysis.get("signals", {}),
        "intent": analysis.get("intent"),
        "confidence": analysis.get("confidence"),
        "explanation": analysis.get("explanation"),
        "outreach_steps": analysis.get("outreach_steps", [])
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True)
    parser.add_argument("--domain", required=False)

    args = parser.parse_args()

    result = run(args.company, args.domain)

    print(json.dumps(result, indent=2))