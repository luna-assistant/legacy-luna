CREATE TABLE IF NOT EXISTS cities (
  id SERIAL PRIMARY KEY,  
  name VARCHAR(255) NOT NULL
  federative_unit_id INTEGER NOT NULL REFERENCES federative_units(id),
);