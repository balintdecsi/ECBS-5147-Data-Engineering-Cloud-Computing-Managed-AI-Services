-- Bucket name: balintd-de1-wikidata
-- Database name: balintd_de1

-- DROP TABLE IF EXISTS balintd_de1.raw_views;

CREATE EXTERNAL TABLE
balintd_de1.raw_views (
    title STRING,
    views INT,
    rank INT,
    date DATE,
    retrieved_at STRING)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://balintd-de1-wikidata/raw-views/'
;