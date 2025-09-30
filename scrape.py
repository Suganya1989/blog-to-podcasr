from __future__ import annotations
import trafilatura
import requests
from bs4 import BeautifulSoup

def extract_from_url(url: str) -> str:
    """Robustly fetch & extract main article text."""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        # fallback: simple HTML text (less clean)
        html = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text("\n", strip=True)
    text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
    return text or ""
