-- TOPIC 3 CRITIC SCORE VS SALES



-- Top-level view of whether critical acclaim translates to sales
SELECT
    gm.score_tier,
    COUNT(DISTINCT f.game_key)             AS game_count,
    ROUND(AVG(f.total_sales)::NUMERIC, 4)  AS avg_sales_millions,
    ROUND(MAX(f.total_sales)::NUMERIC, 4)  AS max_sales_millions,
    ROUND(SUM(f.total_sales)::NUMERIC, 2)  AS total_sales_millions
FROM dw.fact_sales f
JOIN dw.dim_game gm ON f.game_key = gm.game_key
WHERE f.region_key = 1
  AND f.total_sales IS NOT NULL
  AND gm.score_tier != 'Unscored'
GROUP BY gm.score_tier
ORDER BY avg_sales_millions DESC;

-- The "critic-proof" games — massive sales despite mixed/poor reviews
SELECT
    gm.title,
    p.platform_name,
    p.manufacturer,
    g.genre_name,
    d.year,
    f.total_sales,
    f.critic_score,
    gm.score_tier
FROM dw.fact_sales f
JOIN dw.dim_game     gm ON f.game_key     = gm.game_key
JOIN dw.dim_platform p  ON f.platform_key = p.platform_key
JOIN dw.dim_genre    g  ON f.genre_key    = g.genre_key
JOIN dw.dim_date     d  ON f.date_key     = d.date_key
JOIN dw.dim_region   r  ON f.region_key   = r.region_key
WHERE r.region_code = 'NA'
  AND gm.score_tier IN ('Mixed (5-7)', 'Poor (<5)')
  AND f.total_sales IS NOT NULL
ORDER BY f.total_sales DESC
LIMIT 20;
 