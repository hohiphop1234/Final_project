# 🎬 Advanced Movie Recommender System

Hệ thống gợi ý phim thông minh sử dụng **Content-Based Filtering** với **Cosine Similarity** trên MovieLens 100K dataset.

## ✨ Tính Năng Chính

### 🔍 **Movie Search & Recommend**
- Tìm kiếm phim theo tên với similarity scores
- Gợi ý phim tương tự dựa trên cosine similarity
- Hiển thị poster và thông tin chi tiết

### 🎭 **Browse by Genre** 
- Duyệt phim theo thể loại yêu thích
- Hỗ trợ 19 thể loại từ Action đến Western

### 📊 **Dataset Analytics**
- Thống kê tổng quan dataset MovieLens 100K
- Biểu đồ phân tích genres và năm phát hành

### 🎯 **Hybrid Recommendations**
- Kết hợp content-based với user preferences
- Cá nhân hóa dựa trên thể loại và thời gian yêu thích

## 🚀 Cách Chạy

### Setup
1. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Set OMDb API key cho poster chất lượng cao:
   ```bash
   # Tạo file .env
   OMDB_API_KEY=your_key_here
   ```
   Đăng ký miễn phí tại: https://www.omdbapi.com/

### Run Streamlit App
```bash
streamlit run app.py
```

Truy cập: `http://localhost:8501`

## 🧠 Core Algorithm

**Content-Based Filtering** với **TF-IDF** và **Cosine Similarity**:
- Vectorize movie genres sử dụng TF-IDF
- Tính cosine similarity matrix 
- Recommend top-N phim tương tự nhất
- Hybrid approach với user preferences

## 📊 Dataset: MovieLens 100K
- **1,682 phim** với 19 thể loại
- **100,000 ratings** từ 943 users
- Thời gian: 1995-1998


