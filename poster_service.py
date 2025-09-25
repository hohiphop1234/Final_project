import os
import urllib.parse
from functools import lru_cache
from typing import Optional

import requests


def _get_api_key() -> Optional[str]:
    # Prefer environment variable; fallback to .env if python-dotenv is installed
    api_key = os.getenv("OMDB_API_KEY")
    if api_key:
        return api_key
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
        return os.getenv("OMDB_API_KEY")
    except Exception:
        return None


@lru_cache(maxsize=4096)
def get_poster_url(title: str, year: Optional[int] = None) -> Optional[str]:
    """Return a poster URL from OMDb for the given title/year, or None if not found.

    Uses a small LRU cache to reduce API calls.
    """
    api_key = _get_api_key()
    if not api_key:
        return None

    params = {"t": title, "apikey": api_key}
    if year and not (isinstance(year, float) and str(year) == "nan"):
        params["y"] = str(int(year))

    url = "https://www.omdbapi.com/?" + urllib.parse.urlencode(params)
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        poster = data.get("Poster")
        if poster and poster != "N/A":
            return poster
        return None
    except Exception:
        return None