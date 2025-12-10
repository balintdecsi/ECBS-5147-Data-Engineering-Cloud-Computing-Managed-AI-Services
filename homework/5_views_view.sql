    -- DROP VIEW IF EXISTS balintd_de1.views;

CREATE VIEW balintd_de1.views AS
    SELECT
        title,
        views,
        rank,
        date,
        cast(from_iso8601_timestamp(retrieved_at) AS TIMESTAMP) as retrieved_at
    FROM balintd_de1.raw_views
    ORDER BY date, rank
;