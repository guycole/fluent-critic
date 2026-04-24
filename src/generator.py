"""Use OpenAI to generate snarky parody alternative headlines."""

import os

from openai import OpenAI

NUM_ALTERNATIVES = 5


def generate_parody_headlines(headlines: list[str]) -> list[str]:
    """Return NUM_ALTERNATIVES snarky parody headlines based on *headlines*.

    Each generated headline lampoons the breathless, clickbait tone of
    Business Insider while riffing on the actual topics in the source list.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    numbered = "\n".join(f"{i + 1}. {h}" for i, h in enumerate(headlines))

    prompt = (
        "Below are real Business Insider headlines.\n\n"
        f"{numbered}\n\n"
        f"Write exactly {NUM_ALTERNATIVES} extra snarky, satirical parody alternatives "
        "that mock the breathless, hyperbolic, clickbait style of business media. "
        "Each parody headline should:\n"
        "- Exaggerate the drama of the original topics\n"
        "- Use over-the-top financial jargon or corporate buzzwords ironically\n"
        "- Be funny and cutting\n\n"
        f"Output only the {NUM_ALTERNATIVES} headlines, one per line, numbered 1-{NUM_ALTERNATIVES}."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=512,
    )

    raw = response.choices[0].message.content or ""
    parodies: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # Strip leading "1. " numbering if present
        if len(line) > 2 and line[0].isdigit() and ". " in line:
            line = line.split(". ", 1)[1]
        parodies.append(line)

    return parodies[:NUM_ALTERNATIVES]
