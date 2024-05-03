-- Drop the databases if exist.
DROP DATABASE IF EXISTS team8_projectdb CASCADE;
-- DROP DATABASE IF EXISTS team8_projectdb;

-- Create a database teamx_projectdb and access it.
CREATE DATABASE team8_projectdb LOCATION "project/hive/warehouse";
USE team8_projectdb;

-- Create tables

-- links table
DROP TABLE IF EXISTS links;
CREATE EXTERNAL TABLE links
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/links'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/links.avsc');

-- movies table
DROP TABLE IF EXISTS movies;
CREATE EXTERNAL TABLE movies
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/movies'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/movies.avsc');

-- ganres table
DROP TABLE IF EXISTS ganres;
CREATE EXTERNAL TABLE ganres
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/ganres'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/ganres.avsc');

-- ratings table
DROP TABLE IF EXISTS ratings;
CREATE EXTERNAL TABLE ratings
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/ratings'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/ratings.avsc');

-- tags table
DROP TABLE IF EXISTS tags;
CREATE EXTERNAL TABLE tags
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/tags'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/tags.avsc');

-- For checking the content of tables
SELECT * FROM links;
SELECT * FROM movies;
SELECT * FROM ganres;
SELECT * FROM ratings;
SELECT * FROM tags;

--Check datatypes of the columns of the new tables
DESCRIBE links;
DESCRIBE movies;
DESCRIBE ganres;
DESCRIBE ratings;
DESCRIBE tags;

--Ganres table
-- Set the options
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;


-- ALTER TABLE ganres_partitioned DROP IF EXISTS PARTITION (genre STRING)
-- CLUSTERED BY (movieId) INTO 10 BUCKETS
CREATE EXTERNAL TABLE IF NOT EXISTS ganres_partitioned(
    recordId INT,
    movieId INT)
PARTITIONED BY (genre STRING)
STORED AS AVRO LOCATION 'project/hive/warehouse/ganres_partitioned'
TBLPROPERTIES ('AVRO.COMPRESS'='SNAPPY');

INSERT INTO ganres_partitioned
PARTITION (genre)
SELECT recordId, movieId, genre
FROM ganres;

-- Query data from the ganres_partitioned table
SELECT * FROM ganres_partitioned LIMIT 10;

-- Delete table ganres
DROP TABLE IF EXISTS ganres;