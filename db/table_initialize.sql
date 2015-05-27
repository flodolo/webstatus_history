DROP TABLE stats IF EXISTS;
CREATE TABLE stats (
    id integer primary key,
    day varchar(8),
    project_id text,
    locale text,
    fuzzy integer,
    identical integer,
    missing integer,
    percentage real,
    total integer,
    translated integer,
    untranslated integer
);

DROP TABLE projects IF EXISTS;
CREATE TABLE projects (
    project_id text primary key,
    project_name text
);
