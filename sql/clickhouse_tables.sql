CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.raw_product_events
(
 event_id String,
 event_type String,
 user_id String,
 session_id String,
 product_id String,
 amount Float64,
 event_time DateTime
)
ENGINE = MergeTree
ORDER BY (event_time, event_type);

SELECT 
    event_type,
    count() AS event_count
FROM analytics.raw_product_events
GROUP BY event_type
ORDER BY event_count DESC;

SELECT
    product_id,
    sum(amount) AS revenue
FROM analytics.raw_product_events
WHERE event_type = 'purchase'
GROUP BY product_id
ORDER BY revenue DESC;

SELECT
    toStartOfHour(event_time) AS hour,
    count() AS purchase_count
    WHERE event_type = 'purchase'
GROUP BY hour
ORDER BY hour;