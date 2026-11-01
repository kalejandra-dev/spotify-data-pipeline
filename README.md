# Spotify Data Pipeline & API

## Description
An end-to-end Data Engineering project that extracts, transforms, and serves personal Spotify listening history. It features a Pandas-based ETL pipeline, a normalized SQLite relational database, and a containerized FastAPI REST interface.

## Architecture & Tech Stack
- **Data Extraction & Transformation:** Python, Pandas, PyArrow (Parquet)
- **Data Storage:** SQLite (Normalized Relational Schema)
- **API & Data Contracts:** FastAPI, Pydantic
- **Testing:** Pytest, HTTPX
- **Containerization:** Docker

## Project Structure
- `data/`: Raw JSON exports and processed Parquet files (ignored in Git for privacy).
- `src/`: Core logic.
  - `etl.py`: Cleans and filters raw JSON data (drops skips <30s, handles missing values).
  - `database.py`: Loads processed data into a normalized schema (`tracks` and `listens` tables).
  - `queries.py`: Analytical SQL scripts.
  - `api/main.py`: FastAPI endpoints.
- `tests/`: Unit tests for API validation and business logic.

## Installation & Local Execution

1. **Clone the repository and set up the environment:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/spotify-data-pipeline.git](https://github.com/YOUR_USERNAME/spotify-data-pipeline.git)
   cd spotify-data-pipeline
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
