CREATE TABLE IF NOT EXISTS joined_table AS
SELECT *
FROM test_table
LEFT JOIN items_nodup
USING (product_id)
ORDER BY event_time;
