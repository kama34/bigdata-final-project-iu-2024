USE team8_projectdb;

-- Query q5
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
