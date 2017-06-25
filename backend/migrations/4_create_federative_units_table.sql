CREATE TABLE IF NOT EXISTS federative_units (
  id SERIAL PRIMARY KEY,  
  country_id INTEGER NOT NULL REFERENCES countries(id),
  name VARCHAR(255) NOT NULL,
  abbr VARCHAR(3) NOT NULL,
);