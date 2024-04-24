USE team8_projectdb;

-- Query q1
SELECT genre, COUNT(*) as movie_count
FROM ganres_partitioned
GROUP BY genre;

-- Create table q1_results
CREATE TABLE q1_results AS
SELECT genre, COUNT(*) as movie_count
FROM ganres_partitioned
GROUP BY genre;
