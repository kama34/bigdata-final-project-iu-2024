USE team8_projectdb;

-- Query q3
DROP TABLE IF EXISTS q3_results;
CREATE EXTERNAL TABLE q3_results(
userId INT,
rating_count INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 'project/hive/warehouse/q3';

SET hive.resultset.use.unique.column.names = false;

INSERT INTO q3_results
SELECT userId, COUNT(*) as rating_count
FROM ratings
GROUP BY userId;

SELECT * FROM q3_results;