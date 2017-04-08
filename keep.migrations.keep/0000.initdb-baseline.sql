CREATE TABLE IF NOT EXISTS changelog (
    id serial PRIMARY KEY,
    name VARCHAR(64) UNIQUE,
    filenumber VARCHAR(4),
    dateapplied TIMESTAMP,
    comment VARCHAR(255)
);


