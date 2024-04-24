USE team8_projectdb;

-- Query q5
DROP TABLE IF EXISTS q5_results;
CREATE EXTERNAL TABLE q5_results(
userId INT,
unique_movie_count INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 'project/hive/warehouse/q5';

SET hive.resultset.use.unique.column.names = false;

INSERT INTO q5_results
SELECT userId, COUNT(DISTINCT movieId) as unique_movie_count
FROM ratings
GROUP BY userId;

SELECT * FROM q5_results;