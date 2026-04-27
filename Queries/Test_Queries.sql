-- TEST 1: Row counts across all tables 
-- Expected: src should match raw CSV (64,016 rows)
--           fact_sales should be ~4x src (one row per region)
SELECT 'src.raw_video_games' AS table_name, COUNT(*) AS row_count FROM src.raw_video_games
UNION ALL
SELECT 'dw.dim_date',        COUNT(*) FROM dw.dim_date
UNION ALL
SELECT 'dw.dim_platform',    COUNT(*) FROM dw.dim_platform
UNION ALL
SELECT 'dw.dim_publisher',   COUNT(*) FROM dw.dim_publisher
UNION ALL
SELECT 'dw.dim_developer',   COUNT(*) FROM dw.dim_developer
UNION ALL
SELECT 'dw.dim_genre',       COUNT(*) FROM dw.dim_genre
UNION ALL
SELECT 'dw.dim_region',      COUNT(*) FROM dw.dim_region
UNION ALL
SELECT 'dw.dim_game',        COUNT(*) FROM dw.dim_game
UNION ALL
SELECT 'dw.fact_sales',      COUNT(*) FROM dw.fact_sales
ORDER BY table_name;
 
 
-- TEST 2: Orphan check: fact rows with no matching dimension 
-- Expected: all should return 0
SELECT 'missing date_key'      AS check_name, COUNT(*) AS orphan_count
FROM dw.fact_sales f
LEFT JOIN dw.dim_date d ON f.date_key = d.date_key
WHERE d.date_key IS NULL
 
UNION ALL
SELECT 'missing platform_key', COUNT(*)
FROM dw.fact_sales f
LEFT JOIN dw.dim_platform p ON f.platform_key = p.platform_key
WHERE p.platform_key IS NULL
 
UNION ALL
SELECT 'missing publisher_key', COUNT(*)
FROM dw.fact_sales f
LEFT JOIN dw.dim_publisher pb ON f.publisher_key = pb.publisher_key
WHERE pb.publisher_key IS NULL
 
UNION ALL
SELECT 'missing developer_key', COUNT(*)
FROM dw.fact_sales f
LEFT JOIN dw.dim_developer dv ON f.developer_key = dv.developer_key
WHERE dv.developer_key IS NULL
 
UNION ALL
SELECT 'missing genre_key', COUNT(*)
FROM dw.fact_sales f
LEFT JOIN dw.dim_genre g ON f.genre_key = g.genre_key
WHERE g.genre_key IS NULL
 
UNION ALL
SELECT 'missing region_key', COUNT(*)
FROM dw.fact_sales f
LEFT JOIN dw.dim_region r ON f.region_key = r.region_key
WHERE r.region_key IS NULL;
 
 
-- TEST 3: Null sales breakdown
-- Tells us how much of the sales data is missing per region
-- High null counts are expected and documented, just validating
SELECT
    r.region_code,
    COUNT(*)                                        AS total_rows,
    COUNT(f.sales_millions)                         AS non_null_sales,
    COUNT(*) - COUNT(f.sales_millions)              AS null_sales,
    ROUND(
        (COUNT(*) - COUNT(f.sales_millions))::NUMERIC
        / COUNT(*) * 100, 1
    )                                               AS null_pct
FROM dw.fact_sales f
JOIN dw.dim_region r ON f.region_key = r.region_key
GROUP BY r.region_code
ORDER BY r.region_code;