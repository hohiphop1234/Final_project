## Movie Recommender (Streamlit)

Run a simple interface to search and get movie recommendations with posters.

### Setup
1. Create and activate a virtual environment (recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OMDb API key (free at `https://www.omdbapi.com/apikey.aspx`):
   - Option A (recommended): create a `.env` file at project root:
     ```
     OMDB_API_KEY=your_key_here
     ```
   - Option B: set an environment variable `OMDB_API_KEY`.

### Run
```bash
streamlit run app.py
```

Search for a movie in the sidebar; the app shows results and similar titles with posters.


