-- Replace <username> with your username (same as used in the notebook)

-- DROP VIEW IF EXISTS balintd_de1.edits;

CREATE VIEW balintd_de1.edits AS
    SELECT
        title,
        edits,
        date,
        cast(from_iso8601_timestamp(retrieved_at) AS TIMESTAMP) as retrieved_at
    FROM balintd_de1.raw_edits
