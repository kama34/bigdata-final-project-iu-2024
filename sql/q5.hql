USE team8_projectdb;

-- Query q5
SELECT userId, COUNT(DISTINCT movieId) as unique_movie_count
FROM ratings
GROUP BY userId;

-- Create table q5_results
CREATE TABLE q5_results AS
SELECT userId, COUNT(DISTINCT movieId) as unique_movie_count
FROM ratings
GROUP BY userId;
