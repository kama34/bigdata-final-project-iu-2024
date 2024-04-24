USE team8_projectdb;

-- Query q4
SELECT tag, COUNT(*) as tag_count
FROM tags
GROUP BY tag
ORDER BY tag_count DESC;

-- Create table q4_results
CREATE TABLE q4_results AS
SELECT tag, COUNT(*) as tag_count
FROM tags
GROUP BY tag
ORDER BY tag_count DESC;
