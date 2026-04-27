-- TOPIC 1 GAME TRENDS OVER TIME



-- Top genre per era (ranked)
-- Uses RANK() to find the #1 genre in each gaming era
WITH genre_era_sales AS (
    SELECT
        d.gaming_era,
        g.genre_name,
        ROUND(SUM(f.total_sales)::NUMERIC, 2) AS total_sales_millions,
        COUNT(DISTINCT f.game_key)             AS game_count
    FROM dw.fact_sales f
    JOIN dw.dim_date  d ON f.date_key  = d.date_key
    JOIN dw.dim_genre g ON f.genre_key = g.genre_key
    WHERE f.region_key = 1
      AND d.gaming_era != 'Unknown'
      AND f.total_sales IS NOT NULL
    GROUP BY d.gaming_era, g.genre_name
),
ranked AS (
    SELECT *,
        RANK() OVER (PARTITION BY gaming_era ORDER BY total_sales_millions DESC) AS rnk
    FROM genre_era_sales
)
SELECT
    gaming_era,
    genre_name,
    total_sales_millions,
    game_count,
    rnk AS rank_in_era
FROM ranked
WHERE rnk <= 3
ORDER BY gaming_era, rnk;



-- Fastest growing genres (2000s vs 2010s)
SELECT
    g.genre_name,
    ROUND(SUM(CASE WHEN d.decade = 2000 THEN f.total_sales ELSE 0 END)::NUMERIC, 2) AS sales_2000s,
    ROUND(SUM(CASE WHEN d.decade = 2010 THEN f.total_sales ELSE 0 END)::NUMERIC, 2) AS sales_2010s,
    ROUND((
        SUM(CASE WHEN d.decade = 2010 THEN f.total_sales ELSE 0 END) -
        SUM(CASE WHEN d.decade = 2000 THEN f.total_sales ELSE 0 END)
    )::NUMERIC, 2) AS sales_change,
    ROUND((
        (SUM(CASE WHEN d.decade = 2010 THEN f.total_sales ELSE 0 END) -
         SUM(CASE WHEN d.decade = 2000 THEN f.total_sales ELSE 0 END)) /
        NULLIF(SUM(CASE WHEN d.decade = 2000 THEN f.total_sales ELSE 0 END), 0) * 100
    )::NUMERIC, 2) AS pct_change
FROM dw.fact_sales f
JOIN dw.dim_date  d ON f.date_key  = d.date_key
JOIN dw.dim_genre g ON f.genre_key = g.genre_key
WHERE f.region_key = 1
  AND d.decade IN (2000, 2010)
  AND f.total_sales IS NOT NULL
GROUP BY g.genre_name
ORDER BY pct_change DESC NULLS LAST;