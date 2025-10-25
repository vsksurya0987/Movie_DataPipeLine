
import pandas as pd
import requests
from sqlalchemy import create_engine
import sqlite3
import os
import time

# Database
engine = create_engine('sqlite:///movie_pipeline.db')

# Read CSVs
movies_df = pd.read_csv('data/movies.csv')
ratings_df = pd.read_csv('data/ratings.csv')

# Clean & Transform
movies_df['year'] = movies_df['title'].str.extract(r'\((\d{4})\)', expand=False)
movies_df['clean_title'] = movies_df['title'].str.replace(r'\(\d{4}\)', '', regex=True).str.strip()
movies_df['genres_list'] = movies_df['genres'].apply(lambda x: [] if pd.isna(x) else x.split('|'))
movies_df['decade'] = movies_df['year'].apply(lambda y: f"{int(y//10)*10}s" if not pd.isna(y) else None)
ratings_df['rating'] = ratings_df['rating'].astype(float)

# Ratings per movie
ratings_per_movie = ratings_df.groupby('movieId')['rating'].count()
print("Ratings per movie summary:")
print(ratings_per_movie.describe(), "
")

#Identify movies with <5 ratings
few_ratings = ratings_per_movie[ratings_per_movie < 5]
print(f"Movies with less than 5 ratings: {few_ratings.shape[0]}")

# Ratings per user
ratings_per_user = ratings_df.groupby('userId')['rating'].count()
print("Ratings per user summary:")
print(ratings_per_user.describe(), "
")

import pandas as pd
import matplotlib.pyplot as plt

#Rating Distribution
plt.figure(figsize=(8,4))
ratings_df['rating'].hist(bins=10)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.title("Distribution of Ratings")
plt.show()

#Movies per Decade
plt.figure(figsize=(10,5))
movies_df['decade'].value_counts().sort_index().plot(kind='bar')
plt.xlabel("Decade")
plt.ylabel("Number of Movies")
plt.title("Number of Movies per Decade")
plt.show()

# OMDb API (replace with your API key)
OMDB_API_KEY = "your_api_key_here"
def fetch_omdb(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        if data.get('Response') == 'True':
            return {'Director': data.get('Director'),
                    'Plot': data.get('Plot'),
                    'BoxOffice': data.get('BoxOffice')}
        else:
            return {'Director': None,'Plot': None,'BoxOffice': None}
    except:
        return {'Director': None,'Plot': None,'BoxOffice': None}

sample_movies = movies_df.head(10).copy()  # For full dataset, remove .head()
omdb_data = sample_movies['clean_title'].apply(fetch_omdb)
omdb_df = pd.DataFrame(omdb_data.tolist())
enriched_movies = pd.concat([sample_movies, omdb_df], axis=1)

# Load into SQLite
movies_df.to_sql('movies', engine, if_exists='replace', index=False)
ratings_df.to_sql('ratings', engine, if_exists='replace', index=False)
enriched_movies.to_sql('enriched_movies', engine, if_exists='replace', index=False)
print("ETL Completed!")
