-- FRC Scouting System Database Schema
-- 2026 Game: REBUILT

-- Match scouting data table
CREATE TABLE IF NOT EXISTS scouting_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Metadata
    timestamp  TEXT NOT NULL,
    scanned_at TEXT NOT NULL,

    -- Match Information
    match_number  INTEGER NOT NULL,
    team_number   INTEGER NOT NULL,
    alliance      TEXT NOT NULL CHECK(alliance IN ('Red', 'Blue')),
    scouter_name  TEXT NOT NULL,

    -- Pre-Match
    pre_loaded_fuel INTEGER DEFAULT 0 CHECK(pre_loaded_fuel BETWEEN 0 AND 8),

    -- Autonomous
    auto_fuel_active_hub  INTEGER DEFAULT 0,
    auto_tower_level1     INTEGER DEFAULT 0 CHECK(auto_tower_level1 IN (0, 1)),

    -- Teleoperated
    teleop_fuel_active_hub   INTEGER DEFAULT 0,
    teleop_fuel_inactive_hub INTEGER DEFAULT 0,
    fuel_collection_source   TEXT CHECK(fuel_collection_source IN ('Depot', 'Neutral Zone', 'Outpost', '')),

    -- End Game
    max_tower_level TEXT DEFAULT 'None' CHECK(max_tower_level IN ('None', 'Level 1', 'Level 2', 'Level 3')),
    minor_fouls     INTEGER DEFAULT 0,
    major_fouls     INTEGER DEFAULT 0,

    -- Alliance Ranking Points (observed per match)
    energized_rp    INTEGER DEFAULT 0 CHECK(energized_rp    IN (0, 1)),
    supercharged_rp INTEGER DEFAULT 0 CHECK(supercharged_rp IN (0, 1)),
    traversal_rp    INTEGER DEFAULT 0 CHECK(traversal_rp    IN (0, 1)),

    -- Unique constraint: one entry per team per match per alliance
    UNIQUE(match_number, team_number, alliance)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_match_number ON scouting_data(match_number);
CREATE INDEX IF NOT EXISTS idx_team_number  ON scouting_data(team_number);
CREATE INDEX IF NOT EXISTS idx_alliance     ON scouting_data(alliance);
CREATE INDEX IF NOT EXISTS idx_scanned_at   ON scouting_data(scanned_at);

-- Convenience view: per-team aggregates
CREATE VIEW IF NOT EXISTS scouting_summary AS
SELECT
    team_number,
    COUNT(*)                                                      AS matches_played,
    AVG(auto_fuel_active_hub)                                     AS avg_auto_fuel,
    SUM(CASE WHEN auto_tower_level1 = 1 THEN 1 ELSE 0 END) * 1.0
        / COUNT(*)                                                AS auto_tower_rate,
    AVG(teleop_fuel_active_hub)                                   AS avg_teleop_active,
    AVG(teleop_fuel_inactive_hub)                                 AS avg_teleop_inactive,
    AVG(auto_fuel_active_hub + teleop_fuel_active_hub)            AS avg_total_active_hub,
    AVG(CASE max_tower_level
        WHEN 'Level 3' THEN 3
        WHEN 'Level 2' THEN 2
        WHEN 'Level 1' THEN 1
        ELSE 0
    END)                                                          AS avg_tower_level,
    AVG(minor_fouls + major_fouls * 3)                           AS avg_foul_points,
    SUM(CASE WHEN energized_rp    = 1 THEN 1 ELSE 0 END) * 1.0
        / COUNT(*)                                                AS energized_rp_rate,
    SUM(CASE WHEN supercharged_rp = 1 THEN 1 ELSE 0 END) * 1.0
        / COUNT(*)                                                AS supercharged_rp_rate,
    SUM(CASE WHEN traversal_rp    = 1 THEN 1 ELSE 0 END) * 1.0
        / COUNT(*)                                                AS traversal_rp_rate
FROM scouting_data
GROUP BY team_number;

-- Pit scouting data table (unchanged — robot hardware doesn't change per game)
CREATE TABLE IF NOT EXISTS pit_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    team_number        INTEGER NOT NULL UNIQUE,
    robot_weight       REAL    NOT NULL,
    drivetrain_type    TEXT    NOT NULL CHECK(drivetrain_type    IN ('Swerve', 'Tank', 'Mecanum')),
    intake_type        TEXT    NOT NULL CHECK(intake_type        IN ('Over-bumper', 'Through-bumper')),
    programming_language TEXT  NOT NULL CHECK(programming_language IN ('Java', 'C++', 'Python', 'LabVIEW')),
    robot_thumbnail    BLOB,
    scanned_at         TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pit_team_number ON pit_data(team_number);
