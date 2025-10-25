
-- Movie with highest average rating
SELECT m.title, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.movieId
ORDER BY avg_rating DESC
LIMIT 1;

-- Top 5 genres by average rating
SELECT m.main_genre, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.main_genre
ORDER BY avg_rating DESC
LIMIT 5;

-- Director with most movies
SELECT Director, COUNT(*) AS movie_count
FROM enriched_movies
GROUP BY Director
ORDER BY movie_count DESC
LIMIT 1;

-- Average rating per year
SELECT m.year, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.year
ORDER BY m.year;
