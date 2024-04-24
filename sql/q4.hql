USE team8_projectdb;

-- Query q4
DROP TABLE IF EXISTS q4_results;
CREATE EXTERNAL TABLE q4_results(
tag STRING,
tag_count INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 'project/hive/warehouse/q4';

SET hive.resultset.use.unique.column.names = false;

INSERT INTO q4_results
SELECT tag, COUNT(*) as tag_count
FROM tags
GROUP BY tag
ORDER BY tag_count DESC;

SELECT * FROM q4_results;