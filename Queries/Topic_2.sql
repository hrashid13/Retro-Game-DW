-- TOPIC 2 PLATFORM WARS

-- Total sales by manufacturer overall 
SELECT
    p.manufacturer,
    ROUND(SUM(f.total_sales)::NUMERIC, 2)  AS total_sales_millions,
    COUNT(DISTINCT f.game_key)             AS total_titles,
    COUNT(DISTINCT p.platform_key)         AS platform_count,
    ROUND(AVG(f.total_sales)::NUMERIC, 4)  AS avg_sales_per_title
FROM dw.fact_sales f
JOIN dw.dim_platform p ON f.platform_key = p.platform_key
WHERE f.region_key = 1
  AND f.total_sales IS NOT NULL
  AND p.manufacturer IN ('Nintendo', 'Sony', 'Microsoft')
GROUP BY p.manufacturer
ORDER BY total_sales_millions DESC;

-- Ranks every Nintendo/Sony/Microsoft platform into sales quartiles 1 being lowest, 4 being highest
SELECT
    p.manufacturer,
    p.platform_name,
    p.generation,
    p.platform_type,
    ROUND(SUM(f.total_sales)::NUMERIC, 2)  AS total_sales_millions,
    COUNT(DISTINCT f.game_key)             AS title_count,
    NTILE(4) OVER (
        PARTITION BY p.manufacturer
        ORDER BY SUM(f.total_sales)
    )                                      AS sales_quartile
FROM dw.fact_sales f
JOIN dw.dim_platform p ON f.platform_key = p.platform_key
WHERE f.region_key = 1
  AND f.total_sales IS NOT NULL
  AND p.manufacturer IN ('Nintendo', 'Sony', 'Microsoft')
GROUP BY p.manufacturer, p.platform_name, p.generation, p.platform_type
ORDER BY sales_quartile;