USE team8_projectdb;

-- Query q2
CREATE EXTERNAL TABLE q2_results(
movieId INT,
avg_rating FLOAT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 'project/hive/warehouse/q2';

SET hive.resultset.use.unique.column.names = false;

INSERT INTO q2_results
SELECT movieId, AVG(rating) as avg_rating
FROM ratings
GROUP BY movieId;
