CREATE TEMP TABLE temp_test_table AS
SELECT *,
       CASE 
           WHEN EXTRACT(EPOCH FROM event_time - LAG(event_time) OVER (
               PARTITION BY user_id, user_session, product_id, event_type ORDER BY event_time
           )) <= 1
           THEN 1
           ELSE 0
       END AS is_duplicate
FROM test_table;
CREATE TABLE duplicates AS
SELECT *
FROM temp_test_table
WHERE is_duplicate = 1;
ALTER TABLE duplicates
DROP COLUMN is_duplicate;
CREATE TABLE non_duplicates AS
SELECT *
FROM temp_test_table
WHERE is_duplicate = 0
ORDER BY event_time;
ALTER TABLE non_duplicates
DROP COLUMN is_duplicate;
DROP TABLE temp_test_table;
