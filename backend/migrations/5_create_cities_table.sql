CREATE TABLE IF NOT EXISTS cities (
  id SERIAL PRIMARY KEY,  
  federative_unit_id INTEGER NOT NULL REFERENCES federative_units(id),
  name VARCHAR(255) NOT NULL
);