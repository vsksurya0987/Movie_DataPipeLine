
CREATE TABLE movies (
    movieId INTEGER PRIMARY KEY,
    title TEXT,
    genres TEXT,
    year INTEGER,
    clean_title TEXT,
    genres_list TEXT,
    decade TEXT
);

CREATE TABLE ratings (
    userId INTEGER,
    movieId INTEGER,
    rating REAL,
    timestamp INTEGER,
    PRIMARY KEY (userId, movieId)
);

CREATE TABLE enriched_movies (
    movieId INTEGER PRIMARY KEY,
    title TEXT,
    genres TEXT,
    year INTEGER,
    clean_title TEXT,
    genres_list TEXT,
    decade TEXT,
    Director TEXT,
    Plot TEXT,
    BoxOffice TEXT
);
