-- Replace <username> with your username (same as used in the notebook)
-- Bucket name: balintd-de1-wikidata
-- Database name: balintd_de1

-- DROP TABLE IF EXISTS balintd_de1.raw_edits;

CREATE EXTERNAL TABLE
balintd_de1.raw_edits (
    title STRING,
    edits INT,
    date DATE,
    retrieved_at STRING)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://balintd-de1-wikidata/raw-edits/';
