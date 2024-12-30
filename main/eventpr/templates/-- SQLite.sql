-- SQLite
SELECT slug, COUNT(*)
FROM eventapp_event
GROUP BY slug
HAVING COUNT(*) > 1;