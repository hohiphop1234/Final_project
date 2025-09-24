# utils.py
import re
import numpy as np

def extract_year(title: str):
    if not isinstance(title, str):
        return np.nan
    m = re.search(r"\((\d{4})\)", title)
    return int(m.group(1)) if m else np.nan

def row_genres(row, genre_cols):
    g = [g for g in genre_cols if row[g] == 1]
    return "  ".join(g) if g else "unknown"
