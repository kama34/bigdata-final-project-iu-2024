USE team8_projectdb;

-- Query q1
CREATE EXTERNAL TABLE q1_results(
genre STRING,
movie_count INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 'project/hive/warehouse/q1';

SET hive.resultset.use.unique.column.names = false;

INSERT INTO q1_results
SELECT genre, COUNT(*) as movie_count
FROM ganres_partitioned
GROUP BY genre;

SELECT * FROM q1_results;