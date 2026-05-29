import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
DB_DIR = BASE_DIR / "database"

DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "knicks_lineup_intelligence.duckdb"

lineup_file = DATA_DIR / "knicks_lineups_clustered.csv"

conn = duckdb.connect(str(DB_PATH))

conn.execute(f"""
CREATE OR REPLACE TABLE knicks_lineups AS
SELECT *
FROM read_csv_auto('{lineup_file}')
""")

print("Tables loaded:")
print(conn.execute("SHOW TABLES").fetchdf())

print("\nRow count:")
print(conn.execute("""
SELECT COUNT(*) AS row_count
FROM knicks_lineups
""").fetchdf())

print("\nCluster summary:")
print(conn.execute("""
SELECT
    lineup_archetype,
    COUNT(*) AS lineup_count,
    ROUND(AVG(off_rating), 2) AS avg_off_rating,
    ROUND(AVG(def_rating), 2) AS avg_def_rating,
    ROUND(AVG(net_rating), 2) AS avg_net_rating
FROM knicks_lineups
GROUP BY lineup_archetype
ORDER BY avg_net_rating DESC
""").fetchdf())

conn.close()

print("\nDuckDB load complete.")