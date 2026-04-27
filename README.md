# Video Game Sales Data Warehouse

A end-to-end data warehousing project built for ISM 6208 (Data Warehousing) at the University of South Florida. The project models 44 years of global video game sales data (1980–2024) using a three-schema PostgreSQL architecture and a star schema dimensional model.

## Dataset

[Video Game Sales 1980–2024](https://www.kaggle.com/datasets/bhushandivekar/video-game-sales-and-industry-data-1980-2024/data) 
64,016 records covering game titles, platforms, publishers, developers, critic scores, and regional sales across North America, Japan, PAL, and Rest of World.
Data was found at Kaggle

## Architecture

```
src  →  dw  →  agg
```

- **src** — raw staging layer, CSV loaded as-is
- **dw** — star schema with 7 dimensions and 1 fact table
- **agg** — pre-aggregated analytic views

## Schema

**Fact Table**
- `fact_sales` — grain: one row per game × platform × region

**Dimensions**
- `dim_game` — title, score tier (SCD Type 2)
- `dim_platform` — console, manufacturer, type, generation
- `dim_publisher` — publisher name
- `dim_developer` — developer name
- `dim_genre` — genre name and category
- `dim_date` — full date, year, decade, gaming era
- `dim_region` — NA, JP, PAL, Other

## Analytical Queries

Three analytical topics covered in `analytical_queries.sql`:

1. **Genre Trends Over Time**: market share by decade, top genres per era, fastest growing genres
2. **Platform Wars**: Nintendo vs Sony vs Microsoft sales by generation with ROLLUP subtotals
5. **Critic Score vs Sales**: does critical acclaim drive sales? Broken down by genre and platform with CUBE analysis

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- pgAdmin (optional)

### Install dependencies
```bash
pip install pandas psycopg2-binary sqlalchemy python-dotenv
```

### Configure environment
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retro_games_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### Create the database
```bash
psql -U postgres -c "CREATE DATABASE retro_games_db;"
```

### Run the DDL
Run `Schema.sql` in pgAdmin to create the schema structure.

### Run the ETL
```bash
python etl_videogames.py
```

## Files

| File | Description |
|------|-------------|
| `etl_videogames.py` | Main ETL pipeline (src → dw → agg) |
| `Schema.sql` | Schema and table DDL |
| `analytical_queries.sql` | 15 analytical queries across 3 topics |
| `test_queries.sql` | Validation queries to verify the load |
| `.env` | Local credentials (not committed) |

## Course

ISM 6208 — Data Warehousing | University of South Florida | Spring 2026

## Author

**Hesham Rashid**
- Portfolio: https://www.heshamrashid.org/
- LinkedIn: https://www.linkedin.com/in/hesham-rashid/
- Email: h.f.rashid@gmail.com

Master's in AI and Business Analytics - University of South Florida