CREATE TABLE IF NOT EXISTS roles (
  id serial PRIMARY KEY,
  name varchar(50) UNIQUE NOT NULL,
  display_name varchar(100) NOT NULL
);