import argparse
import json

from src.signals import get_signals
from src.llm import analyze
from src.config import PRODUCT_CONTEXT, SIGNAL_DEFINITIONS


def run(company, domain):
    signals = get_signals(company, domain)

    llm_output = analyze(
        company,
        signals,
        PRODUCT_CONTEXT,
        SIGNAL_DEFINITIONS
    )

    # 🔥 Remove outreach if no signals
    if not any([
        llm_output.get("signals", {}).get("hiring"),
        llm_output.get("signals", {}).get("funding"),
        llm_output.get("signals", {}).get("growth_expansion"),
        llm_output.get("signals", {}).get("tech_stack"),
        llm_output.get("signals", {}).get("other"),
    ]):
        llm_output["outreach_steps"] = []

    return {
        "company": company,
        "domain": domain,
        "product_context": PRODUCT_CONTEXT,
        "signals": signals,
        "analysis": llm_output
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True)
    parser.add_argument("--domain", required=False)

    args = parser.parse_args()

    result = run(args.company, args.domain)

    print(json.dumps(result, indent=2))