# cli.py

import json
from src.signals import get_signals

def main():
    print("\n=== Buying Signals CLI ===\n")

    company = input("Company name: ").strip()
    domain = input("Company domain (example.com): ").strip()

    print("\nFetching signals...\n")

    result = get_signals(company, domain)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()