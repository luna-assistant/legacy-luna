CREATE TABLE IF NOT EXISTS contacts (
  id SERIAL PRIMARY KEY,
  person_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
  ddd VARCHAR(3) NOT NULL,
  num VARCHAR(9) NOT NULL
);
