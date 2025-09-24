# utils.py
import re
import numpy as np

def extract_year(title: str):
    """Trích xuất năm từ tiêu đề phim"""
    if not isinstance(title, str):
        return np.nan
    m = re.search(r"\((\d{4})\)", title)
    return int(m.group(1)) if m else np.nan

def row_genres(row, genre_cols):
    """Tạo chuỗi genres từ binary columns"""
    g = [g for g in genre_cols if row[g] == 1]
    return " ".join(g) if g else "unknown"  # Dùng space thay vì double space

def clean_title_for_search(title: str) -> str:
    """Làm sạch title để tìm kiếm tốt hơn"""
    if not isinstance(title, str):
        return ""
    
    # Loại bỏ các ký tự đặc biệt, giữ lại space
    cleaned = re.sub(r"[^\w\s]", " ", title.lower())
    
    # Chuẩn hóa spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    
    return cleaned

def similarity_to_percentage(score: float) -> str:
    """Chuyển similarity score thành percentage string"""
    return f"{score * 100:.1f}%"
