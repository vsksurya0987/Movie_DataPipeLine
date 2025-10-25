

## Overview
This project demonstrates an *end-to-end ETL (Extract, Transform, Load) pipeline* for movie data analysis.  
It integrates data from the *MovieLens dataset (movies.csv and ratings.csv)* and enriches it using the *OMDb API, fetching additional movie details like **Director, Plot, and BoxOffice*.  
The final enriched data is cleaned, transformed, and stored in a *SQLite database*, enabling SQL-based analysis and insights.

---

## Project Workflow

###  1. Extract
- Read data from *movies.csv* and *ratings.csv*.
- Fetch additional data from the *OMDb API* using cleaned movie titles.
- Handle missing or mismatched API results safely.

###  2. Transform
- Extract year from movie titles (e.g., "Toy Story (1995)" → year = 1995).
- Clean movie titles by removing year parentheses.
- Split movie genres into Python lists for analysis.
- Convert lists to strings for database storage.
- Add a new *decade* column for time-based grouping (e.g., "1990s", "2000s").

###  3. Load
- Store cleaned and enriched data into *SQLite* tables:
  - movies
  - ratings
  - enriched_movies
- Ensure *idempotency* (re-running ETL won’t duplicate data).

---

## Database Schema

### movies
| Column | Type | Description |
|--------|------|-------------|
| movieId | INTEGER | Unique movie ID |
| title | TEXT | Full movie title |
| genres | TEXT | Genres string |
| year | INTEGER | Release year |
| clean_title | TEXT | Title without year |
| genres_list | TEXT | Genres as comma-separated values |
| decade | TEXT | Decade label (e.g., 1990s) |

### ratings
| Column | Type | Description |
|--------|------|-------------|
| userId | INTEGER | User ID |
| movieId | INTEGER | Movie ID (foreign key) |
| rating | FLOAT | Rating given by user |
| timestamp | INTEGER | Unix timestamp |

### enriched_movies
| Column | Type | Description |
|--------|------|-------------|
| movieId | INTEGER | Movie ID |
| title | TEXT | Movie title |
| genres | TEXT | Genres string |
| year | INTEGER | Release year |
| clean_title | TEXT | Cleaned title |
| genres_list | TEXT | Genres as string |
| decade | TEXT | Decade |
| Director | TEXT | Director name (from OMDb) |
| Plot | TEXT | Short plot description |
| BoxOffice | TEXT | Box office earnings (from OMDb) |

---

##  Setup Instructions

### Step 1 — Install Required Libraries

# Install required libraries
!pip install pandas sqlalchemy requests

# Imports
import pandas as pd
import requests
from sqlalchemy import create_engine
import sqlite3
import os
import time  # For API rate limiting

pip install pandas sqlalchemy requests

### Step 2 — Run ETL Pipeline
Run the ETL script to extract, clean, enrich, and load data:

python etl.py
This script performs:
- Data extraction from MovieLens CSV files  
- Transformation and cleaning  
- Enrichment using the OMDb API  
- Loading data into a SQLite database (movie_pipeline.db)

### Step 3 — Run SQL Queries
Execute analytical queries stored in queries.sql:

sqlite3 movie_pipeline.db < queries.sql
---

## Design Choices 
- *Database:* SQLite chosen for simplicity and lightweight operation.  
- *Cleaning:* Removed duplicates, handled missing values, standardized titles.  
- *Feature Engineering:* Added a decade column for trend analysis.  
- *Error Handling:* Gracefully handled missing API data and title mismatches.  
- *Idempotency:* Using if_exists='replace' ensures clean re-runs without duplicates.  
- *API Enrichment:* OMDb API used to fetch fields like Director, Plot, BoxOffice.  

---

## Analytical Queries (queries.sql)
1. *Movie with highest average rating*  
2. *Top 5 genres by average rating*  
3. *Director with most movies*  
4. *Average rating per year*

These queries provide insights into:
- Audience preferences  
- High-performing genres  
- Top directors by volume  
- Yearly rating patterns  

---

## Challenges & Solutions

| Challenge | Solution |
|------------|-----------|
| *API Rate Limit* | Tested on a sample of 10 movies; caching can be implemented for full dataset. |
| *Title Mismatch with OMDb* | Cleaned titles and ignored missing ones safely. |
| *SQLite Doesn’t Support Lists* | Converted lists (genres) to comma-separated strings. |
| *Missing API Fields* | Replaced missing values with None and validated data consistency. |

---

##  Output Summary
-  Tables created: movies, ratings, enriched_movies  
-  Clean and complete data after transformation  
-  Successfully executed all analytical queries  
-  Results show top-rated movies, directors, and rating trends  

---

## Repository Structure
movie_data_pipeline/
├── etl.py # Main ETL pipeline (Extract, Transform, Load)
├── schema.sql # CREATE TABLE schema definitions
├── queries.sql # SQL analytical queries
└── README.md # Project documentation




