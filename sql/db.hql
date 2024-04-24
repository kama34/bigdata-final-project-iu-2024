-- Drop the databases if exist.
DROP DATABASE IF EXISTS team8_projectdb;

-- Create a database teamx_projectdb and access it.
CREATE DATABASE team8_projectdb LOCATION "project/hive/warehouse";
USE team8_projectdb;

-- Create tables

-- links table
CREATE EXTERNAL TABLE links
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/links'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/links.avsc');

-- movies table
CREATE EXTERNAL TABLE movies
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/movies'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/movies.avsc');

-- ganres table
CREATE EXTERNAL TABLE ganres
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/ganres'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/ganres.avsc');

-- ratings table
CREATE EXTERNAL TABLE ratings
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/ratings'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/ratings.avsc');

-- tags table
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
CREATE EXTERNAL TABLE ganres_partitioned (
    recordId INT,
    movieId INT,
    genre STRING
)
PARTITIONED BY (genre STRING)
-- CLUSTERED BY (movieId) INTO 10 BUCKETS
STORED AS AVRO
LOCATION 'project/hive/warehouse/team8_projectdb/ganres_partitioned'
TBLPROPERTIES ('avro.schema.url'='project/warehouse/avsc/ganres.avsc');

-- Query data from the ganres_partitioned_and_bucketed table
SELECT * FROM ganres_partitioned LIMIT 10;