USE team8_projectdb;

-- Query q3
SELECT userId, COUNT(*) as rating_count
FROM ratings
GROUP BY userId;

-- Create table q3_results
CREATE TABLE q3_results AS
SELECT userId, COUNT(*) as rating_count
FROM ratings
GROUP BY userId;
