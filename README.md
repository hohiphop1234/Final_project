# 🎬 Movie Recommendation System

A content-based movie recommendation system built with Python and Streamlit that provides personalized movie suggestions based on genre similarity. The application features an intuitive web interface with movie posters and detailed information.

## ✨ Features

- **Smart Search**: Find movies by partial title matching
- **Content-Based Recommendations**: Get similar movies based on genre analysis using TF-IDF and cosine similarity
- **Movie Posters**: Visual movie browsing with automatic poster fetching from OMDb API
- **Interactive Web Interface**: Clean, responsive Streamlit UI
- **MovieLens Dataset**: Built on the reliable MovieLens 100K dataset
- **Customizable Results**: Adjust the number of recommendations (3-20)

## 🏗️ Architecture

The system consists of several key components:

- **Data Processing**: Loads and preprocesses MovieLens 100K dataset
- **Recommendation Engine**: Uses TF-IDF vectorization and cosine similarity for genre-based recommendations
- **Search Module**: Fuzzy title matching for movie discovery
- **Poster Service**: Fetches movie posters from OMDb API
- **Web Interface**: Streamlit-based user interface

## 📊 Dataset

This project uses the **MovieLens 100K dataset**, which contains:
- 100,000 ratings from 943 users on 1,682 movies
- Movie information including titles, genres, and release years
- User demographic information

The dataset is located in the `movielens-100k-dataset/ml-100k/` directory and includes:
- `u.data`: User ratings
- `u.item`: Movie information
- `u.user`: User demographics

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone and Navigate
```bash
git clone <repository-url>
cd Final_project
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure OMDb API (Required for Posters)
Get a free API key from [OMDb API](https://www.omdbapi.com/apikey.aspx)

**Option A (Recommended)**: Create a `.env` file in the project root:
```env
OMDB_API_KEY=your_api_key_here
```

**Option B**: Set environment variable:
```bash
# Windows
set OMDB_API_KEY=your_api_key_here

# macOS/Linux
export OMDB_API_KEY=your_api_key_here
```

## 🏃 Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Interface
1. **Search**: Enter a movie title in the sidebar search box
2. **Adjust Settings**: Use the slider to set the number of recommendations (3-20)
3. **Get Recommendations**: Click "Search & Recommend" to see results
4. **Browse Results**: View search results with posters and movie details
5. **Explore Similar Movies**: Scroll down to see personalized recommendations

## 📁 Project Structure

```
Final_project/
├── app.py                    # Main Streamlit application
├── data_loader.py           # Data loading and preprocessing
├── recommend.py             # Recommendation algorithm
├── search.py               # Movie search functionality
├── poster_service.py       # OMDb API integration for posters
├── config.py              # Configuration and file paths
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── movielens-100k-dataset/  # MovieLens dataset
│   └── ml-100k/
├── processed/            # Preprocessed data files
└── __pycache__/         # Python cache files
```

## 🔧 Core Modules

### `app.py`
- Main Streamlit application with UI components
- Handles user interactions and displays results
- Integrates all modules for complete functionality

### `recommend.py`
- Implements content-based filtering using TF-IDF
- Calculates cosine similarity between movies
- Generates movie recommendations based on genre similarity

### `data_loader.py`
- Loads and preprocesses MovieLens dataset
- Extracts movie years from titles
- Processes genre information
- Saves cleaned data to CSV files

### `search.py`
- Implements fuzzy movie title search
- Returns ranked search results
- Handles partial matches and typos

### `poster_service.py`
- Integrates with OMDb API
- Fetches movie posters and metadata
- Handles API rate limiting and errors

## 🛠️ Dependencies

### Core Libraries
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning algorithms (TF-IDF, cosine similarity)
- **streamlit**: Web application framework

### Additional Libraries
- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management
- **matplotlib & seaborn**: Data visualization
- **jupyter**: Notebook support for development

## 🎯 How It Works

1. **Data Loading**: The system loads the MovieLens 100K dataset and preprocesses it
2. **Feature Extraction**: Movie genres are converted to TF-IDF vectors
3. **Similarity Calculation**: Cosine similarity is computed between all movies
4. **Search**: Users search for movies using partial title matching
5. **Recommendation**: The system finds movies with similar genre profiles
6. **Display**: Results are shown with posters and metadata in a clean interface

## 🔍 Algorithm Details

The recommendation system uses **Content-Based Filtering**:

1. **TF-IDF Vectorization**: Converts movie genres into numerical vectors
2. **Cosine Similarity**: Measures similarity between genre vectors
3. **Ranking**: Sorts movies by similarity score
4. **Filtering**: Returns top-N most similar movies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is for educational purposes. The MovieLens dataset is provided by GroupLens Research and has its own usage terms.

## 🙏 Acknowledgments

- **GroupLens Research** for the MovieLens dataset
- **OMDb API** for movie poster and metadata service
- **Streamlit** for the amazing web framework


