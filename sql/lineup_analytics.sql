-- 1. View all clustered lineups

SELECT *
FROM knicks_lineups;


-- 2. Lineup archetype summary

SELECT
    lineup_archetype,
    COUNT(*) AS lineup_count,
    ROUND(AVG(off_rating), 2) AS avg_off_rating,
    ROUND(AVG(def_rating), 2) AS avg_def_rating,
    ROUND(AVG(net_rating), 2) AS avg_net_rating,
    ROUND(AVG(pace), 2) AS avg_pace,
    ROUND(AVG(ts_pct), 3) AS avg_true_shooting
FROM knicks_lineups
GROUP BY lineup_archetype
ORDER BY avg_net_rating DESC;


-- 3. Best lineups by net rating

SELECT
    group_name,
    lineup_archetype,
    min,
    off_rating,
    def_rating,
    net_rating,
    pace,
    ts_pct
FROM knicks_lineups
ORDER BY net_rating DESC
LIMIT 15;


-- 4. Best defensive lineups

SELECT
    group_name,
    lineup_archetype,
    min,
    def_rating,
    off_rating,
    net_rating
FROM knicks_lineups
ORDER BY def_rating ASC
LIMIT 15;


-- 5. Best offensive lineups

SELECT
    group_name,
    lineup_archetype,
    min,
    off_rating,
    def_rating,
    net_rating
FROM knicks_lineups
ORDER BY off_rating DESC
LIMIT 15;


-- 6. Most-used lineups

SELECT
    group_name,
    lineup_archetype,
    min,
    off_rating,
    def_rating,
    net_rating
FROM knicks_lineups
ORDER BY min DESC
LIMIT 15;


-- 7. High-performing balanced lineups

SELECT
    group_name,
    lineup_archetype,
    min,
    off_rating,
    def_rating,
    net_rating,
    ast_pct,
    reb_pct
FROM knicks_lineups
WHERE off_rating >= 115
  AND def_rating <= 110
  AND net_rating > 0
ORDER BY net_rating DESC;


-- 8. Lineups with strong ball movement

SELECT
    group_name,
    lineup_archetype,
    min,
    ast_pct,
    off_rating,
    net_rating
FROM knicks_lineups
ORDER BY ast_pct DESC
LIMIT 15;