START TRANSACTION;
-- links
CREATE TABLE IF NOT EXISTS links (
    recordId integer NOT NULL  PRIMARY KEY,
    movieId integer, -- foriegin key
    imdbId integer NOT NULL,
    tmdbId real -- one row doesnt have value
);

-- movies
CREATE TABLE IF NOT EXISTS movies (
    -- recordId integer NOT NULL,
    movieId integer NOT NULL  PRIMARY KEY,
    title TEXT NOT NULL
);

-- ganres
CREATE TABLE IF NOT EXISTS ganres (
    recordId integer NOT NULL  PRIMARY KEY,
    movieId integer NOT NULL,
    genre VARCHAR(100) NOT NULL
);

-- ratings
CREATE TABLE IF NOT EXISTS ratings (
    recordId integer NOT NULL  PRIMARY KEY,
    userId integer NOT NULL,
    movieId integer,
    rating real NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- tags
CREATE TABLE IF NOT EXISTS tags (
    recordId integer NOT NULL  PRIMARY KEY,
    userId integer NOT NULL,
    movieId integer,
    tag VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);


-- ALTER TABLE table ADD CONSTRAINT name FOREIGN KEY(mgr) REFERENCES emps (empno);
ALTER TABLE links DROP CONSTRAINT IF EXISTS links_foreign;

ALTER TABLE links ADD CONSTRAINT links_foreign FOREIGN KEY(movieId) REFERENCES movies (movieId);

ALTER TABLE ganres DROP CONSTRAINT IF EXISTS ganres_foreign;

ALTER TABLE ganres ADD CONSTRAINT ganres_foreign FOREIGN KEY(movieId) REFERENCES movies (movieId);

ALTER TABLE ratings DROP CONSTRAINT IF EXISTS ratings_foreign;

ALTER TABLE ratings ADD CONSTRAINT ratings_foreign FOREIGN KEY(movieId) REFERENCES movies (movieId);

ALTER TABLE tags DROP CONSTRAINT IF EXISTS tags_foreign;

ALTER TABLE tags ADD CONSTRAINT tags_foreign FOREIGN KEY(movieId) REFERENCES movies (movieId);

-- ROLLBACK;
COMMIT;

-- links
-- (recordId, movieId, imdbId,tmdbId)
-- movies
-- (movieId,title)
-- ganres
-- (recordId, movieId, genre)
-- ratings
-- (recordId, userId, movieId, rating,timestamp)
-- tags
-- (recordId, userId, movieId,tag)
