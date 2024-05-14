DELETE FROM test_table
WHERE ctid IN (
    SELECT current_ctid
    FROM (
        SELECT 
            ctid AS current_ctid,
            LAG(ctid) OVER (PARTITION BY user_id, user_session, product_id, event_type ORDER BY event_time) AS previous_ctid,
            event_time,
            LAG(event_time) OVER (PARTITION BY user_id, user_session, product_id, event_type ORDER BY event_time) AS prev_event_time,
            EXTRACT(EPOCH FROM event_time - LAG(event_time) OVER (
                PARTITION BY user_id, user_session, product_id, event_type ORDER BY event_time
            )) AS time_diff
        FROM data_2022_oct
    ) AS DupCheck
    WHERE
        prev_event_time IS NOT NULL AND
        ABS(time_diff) <= 1 AND
        current_ctid IS NOT NULL
);