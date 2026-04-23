"""Scrape up to MAX_HEADLINES headlines from the Business Insider homepage."""

import requests
from bs4 import BeautifulSoup

MAX_HEADLINES = 25

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def fetch_headlines(url: str = "https://www.businessinsider.com") -> list[str]:
    """Return up to MAX_HEADLINES unique, non-empty headlines from *url*."""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    seen: set[str] = set()
    headlines: list[str] = []

    # Business Insider uses several anchor / heading patterns; collect all
    # candidate text nodes and deduplicate.
    candidates = soup.find_all(["h2", "h3", "h4"])
    for tag in candidates:
        text = tag.get_text(separator=" ", strip=True)
        if text and text not in seen:
            seen.add(text)
            headlines.append(text)
            if len(headlines) >= MAX_HEADLINES:
                break

    # Fall back to prominent anchor text if headings alone are insufficient.
    if len(headlines) < MAX_HEADLINES:
        for anchor in soup.find_all("a", href=True):
            text = anchor.get_text(separator=" ", strip=True)
            if len(text) > 30 and text not in seen:
                seen.add(text)
                headlines.append(text)
                if len(headlines) >= MAX_HEADLINES:
                    break

    return headlines[:MAX_HEADLINES]
