import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


# CONFIG: credentials loaded from .env file

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "retro_games_db"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}

DATA_PATH = os.getenv("DATA_PATH", "./Data")
CSV_FILE  = "data.csv"

# PLATFORM LOOKUP
# Maps console abbreviation → full name, manufacturer, type, generation

PLATFORM_LOOKUP = {
    # Atari
    "2600":  ("Atari 2600",             "Atari",         "Home Console", "2nd Gen"),
    "5200":  ("Atari 5200",             "Atari",         "Home Console", "2nd Gen"),
    "7800":  ("Atari 7800",             "Atari",         "Home Console", "3rd Gen"),
    "Lynx":  ("Atari Lynx",             "Atari",         "Handheld",     "4th Gen"),
    # Nintendo
    "NES":   ("Nintendo Entertainment System", "Nintendo", "Home Console", "3rd Gen"),
    "FDS":   ("Famicom Disk System",    "Nintendo",      "Home Console", "3rd Gen"),
    "SNES":  ("Super Nintendo",         "Nintendo",      "Home Console", "4th Gen"),
    "VB":    ("Virtual Boy",            "Nintendo",      "Handheld",     "5th Gen"),
    "N64":   ("Nintendo 64",            "Nintendo",      "Home Console", "5th Gen"),
    "GC":    ("GameCube",               "Nintendo",      "Home Console", "6th Gen"),
    "GB":    ("Game Boy",               "Nintendo",      "Handheld",     "4th Gen"),
    "GBC":   ("Game Boy Color",         "Nintendo",      "Handheld",     "5th Gen"),
    "GBA":   ("Game Boy Advance",       "Nintendo",      "Handheld",     "6th Gen"),
    "DS":    ("Nintendo DS",            "Nintendo",      "Handheld",     "7th Gen"),
    "DSi":   ("Nintendo DSi",           "Nintendo",      "Handheld",     "7th Gen"),
    "DSiW":  ("Nintendo DSiWare",       "Nintendo",      "Digital",      "7th Gen"),
    "Wii":   ("Nintendo Wii",           "Nintendo",      "Home Console", "7th Gen"),
    "WiiU":  ("Nintendo Wii U",         "Nintendo",      "Home Console", "8th Gen"),
    "3DS":   ("Nintendo 3DS",           "Nintendo",      "Handheld",     "8th Gen"),
    "NS":    ("Nintendo Switch",        "Nintendo",      "Hybrid",       "9th Gen"),
    "VC":    ("Virtual Console",        "Nintendo",      "Digital",      "7th Gen"),
    "iQue":  ("iQue Player",            "Nintendo",      "Home Console", "6th Gen"),
    # Sony
    "PS":    ("PlayStation",            "Sony",          "Home Console", "5th Gen"),
    "PS2":   ("PlayStation 2",          "Sony",          "Home Console", "6th Gen"),
    "PS3":   ("PlayStation 3",          "Sony",          "Home Console", "7th Gen"),
    "PS4":   ("PlayStation 4",          "Sony",          "Home Console", "8th Gen"),
    "PS5":   ("PlayStation 5",          "Sony",          "Home Console", "9th Gen"),
    "PSP":   ("PlayStation Portable",   "Sony",          "Handheld",     "7th Gen"),
    "PSV":   ("PlayStation Vita",       "Sony",          "Handheld",     "8th Gen"),
    "PSN":   ("PlayStation Network",    "Sony",          "Digital",      "7th Gen"),
    # Microsoft
    "XB":    ("Xbox",                   "Microsoft",     "Home Console", "6th Gen"),
    "X360":  ("Xbox 360",               "Microsoft",     "Home Console", "7th Gen"),
    "XOne":  ("Xbox One",               "Microsoft",     "Home Console", "8th Gen"),
    "XS":    ("Xbox Series X/S",        "Microsoft",     "Home Console", "9th Gen"),
    "XBL":   ("Xbox Live Arcade",       "Microsoft",     "Digital",      "7th Gen"),
    "Series":("Xbox Series X/S",        "Microsoft",     "Home Console", "9th Gen"),
    # Sega
    "GEN":   ("Sega Genesis",           "Sega",          "Home Console", "4th Gen"),
    "MS":    ("Sega Master System",     "Sega",          "Home Console", "3rd Gen"),
    "SAT":   ("Sega Saturn",            "Sega",          "Home Console", "5th Gen"),
    "DC":    ("Sega Dreamcast",         "Sega",          "Home Console", "6th Gen"),
    "GG":    ("Sega Game Gear",         "Sega",          "Handheld",     "4th Gen"),
    "SCD":   ("Sega CD",                "Sega",          "Home Console", "4th Gen"),
    "S32X":  ("Sega 32X",               "Sega",          "Home Console", "5th Gen"),
    # PC / Mobile
    "PC":    ("PC",                     "Various",       "PC",           "N/A"),
    "OSX":   ("Mac OS X",               "Apple",         "PC",           "N/A"),
    "Linux": ("Linux",                  "Various",       "PC",           "N/A"),
    "And":   ("Android",                "Google",        "Mobile",       "N/A"),
    "iOS":   ("iOS",                    "Apple",         "Mobile",       "N/A"),
    "Mob":   ("Mobile (Other)",         "Various",       "Mobile",       "N/A"),
    "WinP":  ("Windows Phone",          "Microsoft",     "Mobile",       "N/A"),
    # NEC
    "PCE":   ("PC Engine / TurboGrafx", "NEC",           "Home Console", "4th Gen"),
    "TG16":  ("TurboGrafx-16",          "NEC",           "Home Console", "4th Gen"),
    "PCFX":  ("PC-FX",                  "NEC",           "Home Console", "5th Gen"),
    # SNK
    "NG":    ("Neo Geo",                "SNK",           "Home Console", "4th Gen"),
    "NGage": ("N-Gage",                 "Nokia",         "Handheld",     "6th Gen"),
    # Retro / Other
    "C64":   ("Commodore 64",           "Commodore",     "PC",           "2nd Gen"),
    "C128":  ("Commodore 128",          "Commodore",     "PC",           "3rd Gen"),
    "Amig":  ("Amiga",                  "Commodore",     "PC",           "3rd Gen"),
    "ApII":  ("Apple II",               "Apple",         "PC",           "2nd Gen"),
    "MSX":   ("MSX",                    "Various",       "PC",           "3rd Gen"),
    "ZXS":   ("ZX Spectrum",            "Sinclair",      "PC",           "3rd Gen"),
    "ACPC":  ("Amstrad CPC",            "Amstrad",       "PC",           "3rd Gen"),
    "BBCM":  ("BBC Micro",              "Acorn",         "PC",           "3rd Gen"),
    "AST":   ("Atari ST",               "Atari",         "PC",           "3rd Gen"),
    "Arc":   ("Acorn Archimedes",       "Acorn",         "PC",           "3rd Gen"),
    "FMT":   ("Fujitsu FM Towns",       "Fujitsu",       "PC",           "4th Gen"),
    "MSD":   ("MS-DOS",                 "Microsoft",     "PC",           "3rd Gen"),
    "Int":   ("Intellivision",          "Mattel",        "Home Console", "2nd Gen"),
    "CV":    ("ColecoVision",           "Coleco",        "Home Console", "2nd Gen"),
    "3DO":   ("3DO Interactive",        "3DO Company",   "Home Console", "5th Gen"),
    "CDi":   ("Philips CD-i",           "Philips",       "Home Console", "5th Gen"),
    "CD32":  ("Amiga CD32",             "Commodore",     "Home Console", "5th Gen"),
    "WS":    ("WonderSwan",             "Bandai",        "Handheld",     "5th Gen"),
    "GIZ":   ("Gizmondo",               "Tiger Telematics","Handheld",   "6th Gen"),
    "OR":    ("Oculus Rift",            "Meta",          "VR",           "N/A"),
    "Ouya":  ("Ouya",                   "Ouya Inc",      "Home Console", "8th Gen"),
    "AJ":    ("Acorn Jupiter",          "Acorn",         "Home Console", "2nd Gen"),
    "Aco":   ("Acorn Electron",         "Acorn",         "PC",           "3rd Gen"),
    "BRW":   ("Bally Astrocade",        "Bally",         "Home Console", "2nd Gen"),
    "WW":    ("WonderSwan Color",       "Bandai",        "Handheld",     "6th Gen"),
    "All":   ("Multi-Platform",         "Various",       "Various",      "N/A"),
}


# CONNECTION

def get_engine():
    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(url)



# STEP 1: CREATE SCHEMAS

def create_schemas(engine):
    print("Creating schemas: src, dw ...")
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS src;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw;"))
    print("  ✓ Schemas ready")



# STEP 2: EXTRACT & LOAD INTO src (raw layer)

SRC_DDL = """
DROP TABLE IF EXISTS src.raw_video_games;
CREATE TABLE src.raw_video_games (
    src_id          SERIAL PRIMARY KEY,
    img             TEXT,
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
    loaded_at       TIMESTAMP DEFAULT NOW()
);
"""

def extract_and_load_src(engine):
    print("\nLoading raw data into src.raw_video_games ...")

    filepath = os.path.join(DATA_PATH, CSV_FILE)
    df = pd.read_csv(filepath, low_memory=False)

    # Drop the img column — not useful for analytics
    df = df.drop(columns=["img"], errors="ignore")

    with engine.begin() as conn:
        conn.execute(text(SRC_DDL))

    df.to_sql(
        "raw_video_games", engine,
        schema="src",
        if_exists="append",
        index=False,
    )
    print(f"  ✓ src.raw_video_games: {len(df)} rows loaded")
    return df



# STEP 3: CREATE DW SCHEMA (star schema DDL)

DW_DDL = """
DROP TABLE IF EXISTS dw.fact_sales          CASCADE;
DROP TABLE IF EXISTS dw.dim_game            CASCADE;
DROP TABLE IF EXISTS dw.dim_platform        CASCADE;
DROP TABLE IF EXISTS dw.dim_publisher       CASCADE;
DROP TABLE IF EXISTS dw.dim_developer       CASCADE;
DROP TABLE IF EXISTS dw.dim_genre           CASCADE;
DROP TABLE IF EXISTS dw.dim_date            CASCADE;
DROP TABLE IF EXISTS dw.dim_region          CASCADE;

-- ── Dimension: Date ───────────────────────────────────────────────
CREATE TABLE dw.dim_date (
    date_key        SERIAL PRIMARY KEY,
    full_date       DATE,
    year            SMALLINT,
    month           SMALLINT,
    month_name      VARCHAR(10),
    quarter         SMALLINT,
    decade          SMALLINT,
    gaming_era      VARCHAR(30)
        -- '2nd Gen (1976-1992)', '3rd/4th Gen (1983-1995)',
        -- '5th Gen (1993-2002)', '6th Gen (1998-2006)',
        -- '7th Gen (2005-2013)', '8th Gen (2012-2020)',
        -- '9th Gen (2020+)', 'Unknown'
);
INSERT INTO dw.dim_date (full_date, year, month, month_name, quarter, decade, gaming_era)
VALUES (NULL, NULL, NULL, 'Unknown', NULL, NULL, 'Unknown');

-- ── Dimension: Platform ───────────────────────────────────────────
CREATE TABLE dw.dim_platform (
    platform_key    SERIAL PRIMARY KEY,
    console_abbr    VARCHAR(20)  NOT NULL UNIQUE,
    platform_name   VARCHAR(100) NOT NULL,
    manufacturer    VARCHAR(50),
    platform_type   VARCHAR(20),   -- Home Console, Handheld, PC, Mobile, Digital, Hybrid, VR
    generation      VARCHAR(20)
);

-- ── Dimension: Publisher ──────────────────────────────────────────
CREATE TABLE dw.dim_publisher (
    publisher_key   SERIAL PRIMARY KEY,
    publisher_name  VARCHAR(200) NOT NULL UNIQUE
);

-- ── Dimension: Developer ──────────────────────────────────────────
CREATE TABLE dw.dim_developer (
    developer_key   SERIAL PRIMARY KEY,
    developer_name  VARCHAR(200) NOT NULL UNIQUE
);

-- ── Dimension: Genre ──────────────────────────────────────────────
CREATE TABLE dw.dim_genre (
    genre_key       SERIAL PRIMARY KEY,
    genre_name      VARCHAR(50)  NOT NULL UNIQUE,
    genre_category  VARCHAR(30)
        -- 'Action', 'Strategy', 'Simulation', 'Sports', 'Other'
);

-- ── Dimension: Game (SCD Type 2) ──────────────────────────────────
-- One row per version of a game record (tracks sales updates over time)
CREATE TABLE dw.dim_game (
    game_key            SERIAL PRIMARY KEY,
    title               VARCHAR(300) NOT NULL,
    score_tier          VARCHAR(20),
        -- 'Acclaimed (8+)', 'Good (7-8)', 'Mixed (5-7)', 'Poor (<5)', 'Unscored'
    -- SCD Type 2 tracking columns
    effective_date      DATE,
    expiry_date         DATE,
    is_current          BOOLEAN DEFAULT TRUE
);

-- ── Dimension: Region ─────────────────────────────────────────────
CREATE TABLE dw.dim_region (
    region_key      SERIAL PRIMARY KEY,
    region_code     VARCHAR(10)  NOT NULL UNIQUE,
    region_name     VARCHAR(50)  NOT NULL,
    region_group    VARCHAR(30)
);

-- ── Fact: Sales ───────────────────────────────────────────────────
-- Grain: one row per game + platform + region + date
CREATE TABLE dw.fact_sales (
    sales_key           SERIAL PRIMARY KEY,
    game_key            INT NOT NULL REFERENCES dw.dim_game(game_key),
    platform_key        INT NOT NULL REFERENCES dw.dim_platform(platform_key),
    publisher_key       INT NOT NULL REFERENCES dw.dim_publisher(publisher_key),
    developer_key       INT NOT NULL REFERENCES dw.dim_developer(developer_key),
    genre_key           INT NOT NULL REFERENCES dw.dim_genre(genre_key),
    date_key            INT NOT NULL REFERENCES dw.dim_date(date_key),
    region_key          INT NOT NULL REFERENCES dw.dim_region(region_key),
    sales_millions      NUMERIC(10,4),   -- NULL = data not collected
    critic_score        NUMERIC(4,2),    -- NULL = unscored
    total_sales         NUMERIC(10,4)
);
"""

def create_dw_schema(engine):
    print("\nCreating dw star schema ...")
    with engine.begin() as conn:
        conn.execute(text(DW_DDL))
    print("  ✓ DW tables created")



# STEP 3b: SEED STATIC DIMENSIONS
# Genre and region don't come from the CSV,
# they are fixed reference data seeded here

def seed_static_dimensions(engine):
    print("\nSeeding static dimensions ...")
    with engine.begin() as conn:

        conn.execute(text("""
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
            ('Unknown',         'Other')
            ON CONFLICT (genre_name) DO NOTHING;
        """))
        print("  ✓ dim_genre seeded")

        conn.execute(text("""
            INSERT INTO dw.dim_region (region_code, region_name, region_group) VALUES
            ('NA',    'North America',       'Americas'),
            ('JP',    'Japan',               'Asia'),
            ('PAL',   'PAL Region (EU/AU)', 'Europe/Oceania'),
            ('OTHER', 'Rest of World',       'Other')
            ON CONFLICT (region_code) DO NOTHING;
        """))
        print("  ✓ dim_region seeded")



# STEP 4: TRANSFORM & LOAD DIMENSIONS

def gaming_era(year):
    if pd.isna(year):
        return "Unknown"
    y = int(year)
    if y < 1983:   return "2nd Gen (1976-1982)"
    elif y < 1993: return "3rd/4th Gen (1983-1992)"
    elif y < 1999: return "5th Gen (1993-1998)"
    elif y < 2006: return "6th Gen (1999-2005)"
    elif y < 2013: return "7th Gen (2006-2012)"
    elif y < 2020: return "8th Gen (2013-2019)"
    else:          return "9th Gen (2020+)"

def score_tier(score):
    if pd.isna(score):
        return "Unscored"
    s = float(score)
    if s >= 8.0:   return "Acclaimed (8+)"
    elif s >= 7.0: return "Good (7-8)"
    elif s >= 5.0: return "Mixed (5-7)"
    else:          return "Poor (<5)"

def genre_category(genre):
    action  = {"Action", "Action-Adventure", "Fighting", "Shooter"}
    strat   = {"Strategy", "Puzzle", "Board Game"}
    sim     = {"Simulation", "Sandbox"}
    sports  = {"Sports", "Racing"}
    social  = {"Party", "Music", "MMO"}
    if genre in action:  return "Action"
    elif genre in strat: return "Strategy"
    elif genre in sim:   return "Simulation"
    elif genre in sports:return "Sports"
    elif genre in social:return "Social"
    else:                return "Other"

def load_dim_date(engine, df):
    print("  Loading dim_date ...")
    df["_parsed_date"] = pd.to_datetime(df["release_date"], dayfirst=True, errors="coerce")
    valid_dates = df["_parsed_date"].dropna().unique()

    rows = []
    for d in valid_dates:
        rows.append({
            "full_date":   d,
            "year":        int(d.year),
            "month":       int(d.month),
            "month_name":  d.strftime("%B"),
            "quarter":     int((d.month - 1) // 3 + 1),
            "decade":      int((d.year // 10) * 10),
            "gaming_era":  gaming_era(d.year),
        })

    date_df = pd.DataFrame(rows).drop_duplicates(subset=["full_date"])
    date_df.to_sql("dim_date", engine, schema="dw", if_exists="append", index=False)
    print(f"    ✓ {len(date_df)} date rows (+ 1 Unknown)")

def load_dim_platform(engine):
    print("  Loading dim_platform ...")
    rows = []
    for abbr, (name, mfr, ptype, gen) in PLATFORM_LOOKUP.items():
        rows.append({
            "console_abbr":  abbr,
            "platform_name": name,
            "manufacturer":  mfr,
            "platform_type": ptype,
            "generation":    gen,
        })
    pd.DataFrame(rows).to_sql(
        "dim_platform", engine, schema="dw", if_exists="append", index=False
    )
    # Insert fallback for any unmapped consoles
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO dw.dim_platform (console_abbr, platform_name, manufacturer, platform_type, generation)
            VALUES ('UNKNOWN', 'Unknown Platform', 'Unknown', 'Unknown', 'Unknown')
            ON CONFLICT (console_abbr) DO NOTHING;
        """))
    print(f"    ✓ {len(rows)} platforms")

def load_dim_publisher(engine, df):
    print("  Loading dim_publisher ...")
    publishers = df["publisher"].fillna("Unknown").unique()
    pub_df = pd.DataFrame({"publisher_name": publishers})
    pub_df.to_sql("dim_publisher", engine, schema="dw", if_exists="append", index=False)
    print(f"    ✓ {len(pub_df)} publishers")

def load_dim_developer(engine, df):
    print("  Loading dim_developer ...")
    developers = df["developer"].fillna("Unknown").unique()
    dev_df = pd.DataFrame({"developer_name": developers})
    dev_df.to_sql("dim_developer", engine, schema="dw", if_exists="append", index=False)
    print(f"    ✓ {len(dev_df)} developers")

def load_dim_game(engine, df):
    print("  Loading dim_game (SCD Type 2) ...")
    df["_parsed_date"]    = pd.to_datetime(df["release_date"], dayfirst=True, errors="coerce")
    df["_parsed_update"]  = pd.to_datetime(df["last_update"],  dayfirst=True, errors="coerce")

    rows = []
    for _, row in df.iterrows():
        effective = row["_parsed_date"].date() if pd.notna(row["_parsed_date"]) else None
        expiry    = row["_parsed_update"].date() if pd.notna(row["_parsed_update"]) else None
        is_cur    = expiry is None   # no update recorded = still current

        rows.append({
            "title":          row["title"],
            "score_tier":     score_tier(row["critic_score"]),
            "effective_date": effective,
            "expiry_date":    expiry,
            "is_current":     is_cur,
        })

    game_df = pd.DataFrame(rows)
    game_df.to_sql("dim_game", engine, schema="dw", if_exists="append", index=False)
    print(f"    ✓ {len(game_df)} game records (SCD Type 2)")

def load_dimensions(engine, df):
    print("\nLoading dimensions ...")
    load_dim_date(engine, df)
    load_dim_platform(engine)
    load_dim_publisher(engine, df)
    load_dim_developer(engine, df)
    load_dim_game(engine, df)



# STEP 5: LOAD FACT TABLE
# Grain: one row per game + platform + region

REGION_SALES_COLS = {
    "NA":    "na_sales",
    "JP":    "jp_sales",
    "PAL":   "pal_sales",
    "OTHER": "other_sales",
}

def load_facts(engine, df):
    print("\nLoading fact_sales ...")

    df["_parsed_date"]   = pd.to_datetime(df["release_date"], dayfirst=True, errors="coerce")
    df["_parsed_update"] = pd.to_datetime(df["last_update"],  dayfirst=True, errors="coerce")

    with engine.begin() as conn:
        dates      = pd.read_sql("SELECT date_key, full_date FROM dw.dim_date", conn)
        platforms  = pd.read_sql("SELECT platform_key, console_abbr FROM dw.dim_platform", conn)
        publishers = pd.read_sql("SELECT publisher_key, publisher_name FROM dw.dim_publisher", conn)
        developers = pd.read_sql("SELECT developer_key, developer_name FROM dw.dim_developer", conn)
        genres     = pd.read_sql("SELECT genre_key, genre_name FROM dw.dim_genre", conn)
        regions    = pd.read_sql("SELECT region_key, region_code FROM dw.dim_region", conn)
        games      = pd.read_sql("SELECT game_key, title, score_tier, effective_date FROM dw.dim_game", conn)

    # Coerce date columns for merging
    dates["full_date"]       = pd.to_datetime(dates["full_date"], errors="coerce")
    games["effective_date"]  = pd.to_datetime(games["effective_date"], errors="coerce")

    df["_publisher"] = df["publisher"].fillna("Unknown")
    df["_developer"] = df["developer"].fillna("Unknown")
    df["_genre"]     = df["genre"].fillna("Unknown")
    df["_console"]   = df["console"].apply(
        lambda x: x if x in PLATFORM_LOOKUP else "UNKNOWN"
    )
    df["_score_tier"] = df["critic_score"].apply(score_tier)

    # Build fact rows per region
    fact_rows = []
    unknown_date_key = int(
        dates[dates["full_date"].isna()]["date_key"].values[0]
    ) if dates["full_date"].isna().any() else 1

    region_map  = dict(zip(regions["region_code"],  regions["region_key"]))
    platform_map= dict(zip(platforms["console_abbr"],platforms["platform_key"]))
    pub_map     = dict(zip(publishers["publisher_name"],publishers["publisher_key"]))
    dev_map     = dict(zip(developers["developer_name"],developers["developer_key"]))
    genre_map   = dict(zip(genres["genre_name"],    genres["genre_key"]))
    date_map    = dict(zip(
        dates["full_date"].dt.date.astype(str),
        dates["date_key"]
    ))

    # Game key lookup by title + score_tier + effective_date
    game_lookup = {}
    for _, g in games.iterrows():
        ed = str(g["effective_date"].date()) if pd.notna(g["effective_date"]) else "NaT"
        game_lookup[(g["title"], g["score_tier"], ed)] = g["game_key"]

    for _, row in df.iterrows():
        ed_str = str(row["_parsed_date"].date()) if pd.notna(row["_parsed_date"]) else "NaT"
        game_key = game_lookup.get(
            (row["title"], row["_score_tier"], ed_str)
        )
        if game_key is None:
            continue

        date_str = str(row["_parsed_date"].date()) if pd.notna(row["_parsed_date"]) else "None"
        date_key = date_map.get(date_str, unknown_date_key)

        platform_key  = platform_map.get(row["_console"])
        publisher_key = pub_map.get(row["_publisher"])
        developer_key = dev_map.get(row["_developer"])
        genre_key     = genre_map.get(row["_genre"])

        if not all([platform_key, publisher_key, developer_key, genre_key]):
            continue

        for region_code, sales_col in REGION_SALES_COLS.items():
            fact_rows.append({
                "game_key":      int(game_key),
                "platform_key":  int(platform_key),
                "publisher_key": int(publisher_key),
                "developer_key": int(developer_key),
                "genre_key":     int(genre_key),
                "date_key":      int(date_key),
                "region_key":    int(region_map[region_code]),
                "sales_millions":row[sales_col] if pd.notna(row[sales_col]) else None,
                "critic_score":  row["critic_score"] if pd.notna(row["critic_score"]) else None,
                "total_sales":   row["total_sales"] if pd.notna(row["total_sales"]) else None,
            })

    fact_df = pd.DataFrame(fact_rows)
    fact_df.to_sql(
        "fact_sales", engine, schema="dw",
        if_exists="append", index=False, chunksize=5000
    )
    print(f"  ✓ fact_sales: {len(fact_df)} rows loaded ({len(df)} source rows × 4 regions)")





# MAIN

if __name__ == "__main__":
    print("=" * 55)
    print("Video Game Sales ETL Pipeline")
    print("=" * 55)

    engine = get_engine()

    create_schemas(engine)
    raw_df = extract_and_load_src(engine)
    create_dw_schema(engine)
    seed_static_dimensions(engine)
    load_dimensions(engine, raw_df)
    load_facts(engine, raw_df)
  

    print("\n" + "=" * 55)
    print("ETL complete.  Schemas: src | dw ")
    print("  src.raw_video_games     — raw source data")
    print("  dw.dim_date             — date + gaming era")
    print("  dw.dim_platform         — console + manufacturer + type + gen")
    print("  dw.dim_publisher        — publisher")
    print("  dw.dim_developer        — developer")
    print("  dw.dim_genre            — genre + category")
    print("  dw.dim_game             — game title + score tier (SCD Type 2)")
    print("  dw.dim_region           — NA / JP / PAL / Other")
    print("  dw.fact_sales           — grain: game × platform × region")
    print("=" * 55)