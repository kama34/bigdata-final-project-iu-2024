-- always test if you can import the data from PgAdmin then you automate it by writing the script
COPY movies (movieId,title) FROM STDIN WITH CSV HEADER DELIMITER ',' NULL AS '';
COPY links (movieId, imdbId,tmdbId,recordId) FROM STDIN WITH CSV HEADER DELIMITER ',' NULL AS '';
COPY ratings (userId, movieId, rating,timestamp,recordId) FROM STDIN WITH CSV HEADER DELIMITER ',' NULL AS '';
COPY tags (userId, movieId,tag,timestamp,recordId) FROM STDIN WITH CSV HEADER DELIMITER ',' NULL AS '';
COPY ganres (recordId, movieId, genre) FROM STDIN WITH CSV HEADER DELIMITER ',' NULL AS '';

-- COPY movies FROM STDIN WITH CSV HEADER DELIMITER ',' QUOTE '\'' NULL AS 'null';
-- COPY links FROM STDIN WITH CSV HEADER DELIMITER ',' QUOTE '\''  NULL AS 'null';
-- COPY ratings FROM STDIN WITH CSV HEADER DELIMITER ',' QUOTE '\'' NULL AS 'null';
-- COPY tags FROM STDIN WITH CSV HEADER DELIMITER ',' QUOTE '\'' NULL AS 'null';
-- COPY ganres FROM STDIN WITH CSV HEADER DELIMITER ',' QUOTE '\'' NULL AS 'null';
