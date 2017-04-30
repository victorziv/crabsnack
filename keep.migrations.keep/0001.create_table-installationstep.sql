CREATE TABLE IF NOT EXISTS installationstep (
    id serial PRIMARY KEY,
    name VARCHAR(32) UNIQUE,
    display_name VARCHAR(64),
    priority INTEGER
);
