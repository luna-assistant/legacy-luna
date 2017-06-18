CREATE TABLE IF NOT EXISTS users (
  id serial PRIMARY KEY,
  username varchar(100) UNIQUE NOT NULL,
  password varchar(72) NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL,
  deleted_at timestamp NULL
);