#!/usr/bin/env python3
"""fluent-critic: Business Insider PitchBot.

Scrapes up to 25 headlines from Business Insider and uses OpenAI to produce
5 snarky parody alternatives.

Usage
-----
Ensure OPENAI_API_KEY is set (e.g. via a .env file), then run:

    python src/main.py
"""

import sys

from dotenv import load_dotenv

from scraper import fetch_headlines
from generator import generate_parody_headlines


def main() -> None:
    # Load environment variables from a .env file if present
    load_dotenv()

    print("=== Business Insider PitchBot ===\n")

    print("Fetching headlines from Business Insider…")
    try:
        headlines = fetch_headlines()
    except Exception as exc:
        print(f"ERROR: Could not fetch headlines – {exc}", file=sys.stderr)
        sys.exit(1)

    if not headlines:
        print("ERROR: No headlines found.", file=sys.stderr)
        sys.exit(1)

    print(f"\nCollected {len(headlines)} headline(s):\n")
    for i, h in enumerate(headlines, 1):
        print(f"  {i:2}. {h}")

    print("\nGenerating snarky parody headlines via OpenAI…\n")
    try:
        parodies = generate_parody_headlines(headlines)
    except Exception as exc:
        print(f"ERROR: Could not generate parodies – {exc}", file=sys.stderr)
        sys.exit(1)

    print("=== Parody Alternatives ===\n")
    for i, p in enumerate(parodies, 1):
        print(f"  {i}. {p}")

    print()


if __name__ == "__main__":
    main()
