"""Unit tests for fluent-critic."""

import sys
import os
from unittest.mock import MagicMock, patch

import pytest

# Allow tests to import from src/ without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


# ---------------------------------------------------------------------------
# scraper tests
# ---------------------------------------------------------------------------

SAMPLE_HTML = """
<html><body>
  <h2>Apple's iPhone Sales Collapse: The End of an Era?</h2>
  <h3>Wall Street Braces for Another Wild Week</h3>
  <h4>Why Every CEO Is Suddenly Talking About AI</h4>
  <h2>The 10 Best-Paying Remote Jobs You Can Get Right Now</h2>
  <a href="/story">A really long anchor text that should also be included if headings run out of steam here</a>
</body></html>
"""


def _make_mock_response(html: str, status_code: int = 200):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.text = html
    mock_resp.raise_for_status = MagicMock()
    return mock_resp


class TestFetchHeadlines:
    def test_returns_list(self):
        from scraper import fetch_headlines

        with patch("scraper.requests.get", return_value=_make_mock_response(SAMPLE_HTML)):
            result = fetch_headlines()
        assert isinstance(result, list)

    def test_extracts_headings(self):
        from scraper import fetch_headlines

        with patch("scraper.requests.get", return_value=_make_mock_response(SAMPLE_HTML)):
            result = fetch_headlines()
        assert len(result) >= 4
        assert any("iPhone" in h for h in result)
        assert any("Wall Street" in h for h in result)

    def test_max_headlines_limit(self):
        """Result must never exceed MAX_HEADLINES (25)."""
        from scraper import fetch_headlines, MAX_HEADLINES

        # Build an HTML page with 50 headings
        many_headings = "".join(f"<h2>Headline number {i}</h2>" for i in range(50))
        html = f"<html><body>{many_headings}</body></html>"

        with patch("scraper.requests.get", return_value=_make_mock_response(html)):
            result = fetch_headlines()
        assert len(result) <= MAX_HEADLINES

    def test_deduplication(self):
        """Duplicate headings must appear only once."""
        from scraper import fetch_headlines

        dup_html = "<html><body>" + "<h2>Duplicate Headline</h2>" * 10 + "</body></html>"
        with patch("scraper.requests.get", return_value=_make_mock_response(dup_html)):
            result = fetch_headlines()
        assert result.count("Duplicate Headline") == 1

    def test_http_error_propagates(self):
        """A network error should bubble up so main.py can handle it."""
        import requests as req
        from scraper import fetch_headlines

        with patch("scraper.requests.get", side_effect=req.exceptions.ConnectionError("down")):
            with pytest.raises(req.exceptions.ConnectionError):
                fetch_headlines()


# ---------------------------------------------------------------------------
# generator tests
# ---------------------------------------------------------------------------

class TestGenerateParodyHeadlines:
    def _patched_openai(self, lines: list[str]):
        """Return a context-manager patch that makes the OpenAI client return *lines*."""
        mock_content = "\n".join(f"{i + 1}. {l}" for i, l in enumerate(lines))

        mock_choice = MagicMock()
        mock_choice.message.content = mock_content

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        return patch("generator.OpenAI", return_value=mock_client)

    def test_returns_list(self):
        from generator import generate_parody_headlines, NUM_ALTERNATIVES

        fake_lines = [f"Parody {i}" for i in range(NUM_ALTERNATIVES)]
        with self._patched_openai(fake_lines):
            with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
                result = generate_parody_headlines(["Real headline"] * 5)
        assert isinstance(result, list)

    def test_returns_five_headlines(self):
        from generator import generate_parody_headlines, NUM_ALTERNATIVES

        fake_lines = [f"Parody {i}" for i in range(NUM_ALTERNATIVES)]
        with self._patched_openai(fake_lines):
            with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
                result = generate_parody_headlines(["Real headline"] * 25)
        assert len(result) == NUM_ALTERNATIVES

    def test_numbering_stripped(self):
        """Leading '1. ' numbering should be stripped from each parody."""
        from generator import generate_parody_headlines

        fake_lines = ["Parody one", "Parody two", "Parody three", "Parody four", "Parody five"]
        with self._patched_openai(fake_lines):
            with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
                result = generate_parody_headlines(["Headline"] * 25)
        for item in result:
            assert not item[0].isdigit(), f"Numbering not stripped: {item!r}"

    def test_missing_api_key_raises(self):
        """Missing OPENAI_API_KEY should cause a KeyError."""
        from generator import generate_parody_headlines

        env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(KeyError):
                generate_parody_headlines(["Headline"] * 5)
