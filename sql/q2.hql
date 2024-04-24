USE team8_projectdb;

-- Query q2
SELECT movieId, AVG(rating) as avg_rating
FROM ratings
GROUP BY movieId;

-- Create table q2_results
CREATE TABLE q2_results AS
SELECT movieId, AVG(rating) as avg_rating
FROM ratings
GROUP BY movieId;
