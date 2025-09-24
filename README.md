# 🎬 Advanced Movie Recommender System

A content-based movie recommendation system using the MovieLens 100K dataset. The system uses TF-IDF vectorization and cosine similarity to recommend movies based on genre similarity, with both a Streamlit web interface and comprehensive analysis tools.

## ✨ Features

### 🔍 **Movie Search & Recommend**
- **Content-based recommendations** using TF-IDF and cosine similarity
- **Interactive Streamlit web app** with movie posters
- **Movie search functionality** with fuzzy matching
- Hiển thị poster và thông tin chi tiết với similarity scores

### 🎭 **Browse by Genre** 
- **Data visualization** and analysis tools
- Duyệt phim theo thể loại yêu thích
- Hỗ trợ 19 thể loại từ Action đến Western

### 📊 **Dataset Analytics**
- Thống kê tổng quan dataset MovieLens 100K
- Biểu đồ phân tích genres và năm phát hành
- **Jupyter notebook** for data exploration and development

### 🎯 **Hybrid Recommendations**
- Kết hợp content-based với user preferences
- Cá nhân hóa dựa trên thể loại và thời gian yêu thích
- **Standalone Python script** for command-line usage

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Final_project
```

### 2. Create Virtual Environment

#### On Windows (PowerShell):
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### On Windows (Command Prompt):
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate.bat
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### 4. Set Up OMDb API Key
Get a free API key from [OMDb API](https://www.omdbapi.com/apikey.aspx) for movie posters and metadata.

**Option A (Recommended)**: Create a `.env` file in the project root:
```bash
OMDB_API_KEY=your_api_key_here
```

**Option B**: Set environment variable:
- **Windows**: `set OMDB_API_KEY=your_api_key_here`
- **macOS/Linux**: `export OMDB_API_KEY=your_api_key_here`

### 5. Verify Installation
```bash
# Test that all packages are installed correctly
python -c "import pandas, numpy, sklearn, streamlit; print('All dependencies installed successfully!')"
```

## Usage

### Streamlit Web App
Run the interactive web interface:
```bash
streamlit run app.py
```

Truy cập: `http://localhost:8501`

Then open your browser to view:
- Search for movies in the sidebar
- View movie recommendations with posters
- Explore similar movies based on genre similarity

### Jupyter Notebook
Launch Jupyter to explore the data and development process:
```bash
jupyter notebook "Copy_of_demo (1).ipynb"
```

### Python Script
Run the standalone recommendation system:
```bash
python movie_recommendation_system.py
```

This provides:
- Dataset information and statistics
- Sample recommendations
- Interactive command-line interface

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

## Project Structure

```
Final_project/
├── .venv/                          # Virtual environment
├── .env                            # Environment variables (create this)
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── app.py                          # Streamlit web application
├── movie_recommendation_system.py  # Standalone Python script
├── Copy_of_demo (1).ipynb         # Jupyter notebook
├── movielens-100k-dataset/        # MovieLens dataset
└── processed/                      # Processed CSV files
```

## Dependencies

- **pandas** & **numpy**: Data manipulation and analysis
- **scikit-learn**: Machine learning (TF-IDF, cosine similarity)
- **matplotlib** & **seaborn**: Data visualization
- **streamlit**: Web application framework
- **requests**: HTTP requests for movie posters
- **python-dotenv**: Environment variable management
- **jupyter**: Interactive notebook environment

## Virtual Environment Management

### Deactivate Virtual Environment
```bash
deactivate
```

### Reactivate Virtual Environment
#### Windows (PowerShell):
```bash
.\.venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt):
```bash
.\.venv\Scripts\activate.bat
```

#### macOS/Linux:
```bash
source .venv/bin/activate
```

### Update Dependencies
```bash
# After activating virtual environment
pip install --upgrade -r requirements.txt
```

### Add New Dependencies
```bash
# Install new package
pip install package_name

# Update requirements file
pip freeze > requirements.txt
```

## Troubleshooting

### Virtual Environment Issues
- **Permission Error on Windows**: Run PowerShell as Administrator or change execution policy
- **Command not found**: Ensure Python is installed and added to PATH
- **Package conflicts**: Delete `.venv` folder and recreate the virtual environment

### Missing Dataset
If the MovieLens dataset is missing, the notebook includes instructions to download it using the `opendatasets` library.

### API Key Issues
- Ensure your OMDb API key is valid and not expired
- Check that the `.env` file is in the project root directory
- Verify the environment variable is set correctly

## Development

### Setting Up Development Environment
1. Follow the setup instructions above
2. Install additional development dependencies (if any):
   ```bash
   pip install -r requirements-dev.txt  # if available
   ```
3. Run tests (if available):
   ```bash
   python -m pytest
   ```

### Contributing
1. Create a new branch for your feature
2. Make your changes
3. Test your changes thoroughly
4. Submit a pull request

## License

This project is for educational purposes. The MovieLens dataset is provided by GroupLens Research at the University of Minnesota.


