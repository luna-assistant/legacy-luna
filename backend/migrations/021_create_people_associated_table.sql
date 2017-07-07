CREATE TABLE IF NOT EXISTS people_associated (
  id SERIAL PRIMARY KEY,
  person_id INTEGER NOT NULL REFERENCES people(id),
  associated_id INTEGER NOT NULL REFERENCES people(id)
);
