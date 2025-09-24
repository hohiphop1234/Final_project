import os
import urllib.parse
from functools import lru_cache
from typing import Optional
import streamlit as st
import requests

# Fallback poster URLs cho demo
FALLBACK_POSTERS = {
    "toy story": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_SX300.jpg",
    "jumanji": "https://m.media-amazon.com/images/M/MV5BZTk2ZmUwYmEtNTcwZS00YmMyLWFkYjMtNTRmZDA3YWExMjc2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
    "grumpier old men": "https://m.media-amazon.com/images/M/MV5BMjQxM2YyNjMtZjUxYy00OGYyLTg0MmQtNGE2YzNjYmUyZTY1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
    "waiting to exhale": "https://m.media-amazon.com/images/M/MV5BYzcxMjdkOTQtNDVmMS00NzQ1LWIwNjYtZjI4ODEzMzY0MjNjXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
    "father of the bride part ii": "https://m.media-amazon.com/images/M/MV5BMTkzMzE0MjAzN15BMl5BanBnXkFtZTcwNzQ0MDEzMQ@@._V1_SX300.jpg",
    "heat": "https://m.media-amazon.com/images/M/MV5BNDc0YjFhOGItZjljZC00ZmM4LWFkODgtNmNjZTJhNGY5Y2QwXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
    "sabrina": "https://m.media-amazon.com/images/M/MV5BYWNmOGVjNmItNzUwZi00NzIwLWE5NjgtYTgyNGI3ODA3NDczXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
    "goldeneye": "https://m.media-amazon.com/images/M/MV5BMzk2OTg4MTk1NF5BMl5BanBnXkFtZTcwNjExNTgzNA@@._V1_SX300.jpg",
    "american president": "https://m.media-amazon.com/images/M/MV5BYTk1MWVhN2MtNzNjYi00NGJjLWE2MTYtNzE2ZTdjOGRmNzk1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
    "dracula: dead and loving it": "https://m.media-amazon.com/images/M/MV5BMTU2MDAwOTcyN15BMl5BanBnXkFtZTcwMDM2OTM3OA@@._V1_SX300.jpg"
}

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

def get_placeholder_poster(title: str) -> str:
    """Tạo placeholder poster với màu ngẫu nhiên"""
    title_encoded = title.replace(" ", "+")
    colors = ["4CAF50", "2196F3", "FF9800", "E91E63", "9C27B0", "00BCD4"]
    color = colors[hash(title) % len(colors)]
    return f"https://via.placeholder.com/300x450/{color}/FFFFFF?text={title_encoded}"

@lru_cache(maxsize=4096)
def get_poster_url(title: str, year: Optional[int] = None) -> Optional[str]:
    """Return a poster URL from OMDb for the given title/year, or fallback options."""
    
    # Kiểm tra fallback posters trước (cho demo)
    title_lower = title.lower().strip()
    if title_lower in FALLBACK_POSTERS:
        return FALLBACK_POSTERS[title_lower]
    
    # Thử OMDb API nếu có key
    api_key = _get_api_key()
    if api_key:
        params = {"t": title, "apikey": api_key}
        if year and not (isinstance(year, float) and str(year) == "nan"):
            params["y"] = str(int(year))

        url = "https://www.omdbapi.com/?" + urllib.parse.urlencode(params)
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                poster = data.get("Poster")
                if poster and poster != "N/A":
                    return poster
        except Exception:
            pass
    
    # Fallback: placeholder poster
    return get_placeholder_poster(title)


