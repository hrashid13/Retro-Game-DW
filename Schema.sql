-- Create Schemas
CREATE SCHEMA IF NOT EXISTS src;
CREATE SCHEMA IF NOT EXISTS dw;
CREATE SCHEMA IF NOT EXISTS agg;



-- SRC SCHEMA — Raw staging layer


DROP TABLE IF EXISTS src.raw_video_games;

CREATE TABLE src.raw_video_games (
    src_id          SERIAL          PRIMARY KEY,
    title           VARCHAR(300),
    console         VARCHAR(20),
    genre           VARCHAR(50),
    publisher       VARCHAR(200),
    developer       VARCHAR(200),
    critic_score    NUMERIC(4,2),
    total_sales     NUMERIC(10,4),
    na_sales        NUMERIC(10,4),
    jp_sales        NUMERIC(10,4),
    pal_sales       NUMERIC(10,4),
    other_sales     NUMERIC(10,4),
    release_date    VARCHAR(20),
    last_update     VARCHAR(20),
    loaded_at       TIMESTAMP       DEFAULT NOW()
);



-- DW SCHEMA — Star schema layer

-- Drop tables in dependency order 
DROP TABLE IF EXISTS dw.fact_sales      CASCADE;
DROP TABLE IF EXISTS dw.dim_game        CASCADE;
DROP TABLE IF EXISTS dw.dim_platform    CASCADE;
DROP TABLE IF EXISTS dw.dim_publisher   CASCADE;
DROP TABLE IF EXISTS dw.dim_developer   CASCADE;
DROP TABLE IF EXISTS dw.dim_genre       CASCADE;
DROP TABLE IF EXISTS dw.dim_date        CASCADE;
DROP TABLE IF EXISTS dw.dim_region      CASCADE;


-- dim_date 
CREATE TABLE dw.dim_date (
    date_key        SERIAL          PRIMARY KEY,
    full_date       DATE,
    year            SMALLINT,
    month           SMALLINT,
    month_name      VARCHAR(10),
    quarter         SMALLINT,
    decade          SMALLINT,
    gaming_era      VARCHAR(30)
);

-- Unknown date surrogate (date_key = 1)
INSERT INTO dw.dim_date (full_date, year, month, month_name, quarter, decade, gaming_era)
VALUES (NULL, NULL, NULL, 'Unknown', NULL, NULL, 'Unknown');


-- dim_platform 
CREATE TABLE dw.dim_platform (
    platform_key    SERIAL          PRIMARY KEY,
    console_abbr    VARCHAR(20)     NOT NULL UNIQUE,
    platform_name   VARCHAR(100)    NOT NULL,
    manufacturer    VARCHAR(50),
    platform_type   VARCHAR(20),
    generation      VARCHAR(20)
);


-- dim_publisher 
CREATE TABLE dw.dim_publisher (
    publisher_key   SERIAL          PRIMARY KEY,
    publisher_name  VARCHAR(200)    NOT NULL UNIQUE
);


-- Seed the Unknown fallback
INSERT INTO dw.dim_publisher (publisher_name) VALUES ('Unknown');


--  dim_developer 
CREATE TABLE dw.dim_developer (
    developer_key   SERIAL          PRIMARY KEY,
    developer_name  VARCHAR(200)    NOT NULL UNIQUE
);


-- Seed the Unknown fallback
INSERT INTO dw.dim_developer (developer_name) VALUES ('Unknown');


-- dim_genre
CREATE TABLE dw.dim_genre (
    genre_key       SERIAL          PRIMARY KEY,
    genre_name      VARCHAR(50)     NOT NULL UNIQUE,
    genre_category  VARCHAR(30)
);

INSERT INTO dw.dim_genre (genre_name, genre_category) VALUES
('Action',          'Action'),
('Action-Adventure','Action'),
('Adventure',       'Action'),
('Fighting',        'Action'),
('Shooter',         'Action'),
('Platform',        'Action'),
('Strategy',        'Strategy'),
('Puzzle',          'Strategy'),
('Board Game',      'Strategy'),
('Role-Playing',    'Other'),
('Simulation',      'Simulation'),
('Sandbox',         'Simulation'),
('Sports',          'Sports'),
('Racing',          'Sports'),
('Party',           'Social'),
('Music',           'Social'),
('MMO',             'Social'),
('Visual Novel',    'Other'),
('Education',       'Other'),
('Misc',            'Other'),
('Unknown',         'Other');


-- dim_region 
CREATE TABLE dw.dim_region (
    region_key      SERIAL          PRIMARY KEY,
    region_code     VARCHAR(10)     NOT NULL UNIQUE,
    region_name     VARCHAR(50)     NOT NULL,
    region_group    VARCHAR(30)
);

INSERT INTO dw.dim_region (region_code, region_name, region_group) VALUES
('NA',    'North America',       'Americas'),
('JP',    'Japan',               'Asia'),
('PAL',   'PAL Region (EU/AU)', 'Europe/Oceania'),
('OTHER', 'Rest of World',       'Other');


-- dim_game (SCD Type 2) 
CREATE TABLE dw.dim_game (
    game_key        SERIAL          PRIMARY KEY,
    title           VARCHAR(300)    NOT NULL,
    score_tier      VARCHAR(20),
    effective_date  DATE,
    expiry_date     DATE,
    is_current      BOOLEAN         DEFAULT TRUE
);




--  fact_sales 
-- Grain: one row per game × platform × region
CREATE TABLE dw.fact_sales (
    sales_key           SERIAL      PRIMARY KEY,
    game_key            INT         NOT NULL REFERENCES dw.dim_game(game_key),
    platform_key        INT         NOT NULL REFERENCES dw.dim_platform(platform_key),
    publisher_key       INT         NOT NULL REFERENCES dw.dim_publisher(publisher_key),
    developer_key       INT         NOT NULL REFERENCES dw.dim_developer(developer_key),
    genre_key           INT         NOT NULL REFERENCES dw.dim_genre(genre_key),
    date_key            INT         NOT NULL REFERENCES dw.dim_date(date_key),
    region_key          INT         NOT NULL REFERENCES dw.dim_region(region_key),
    sales_millions      NUMERIC(10,4),
    critic_score        NUMERIC(4,2),
    total_sales         NUMERIC(10,4)
);
