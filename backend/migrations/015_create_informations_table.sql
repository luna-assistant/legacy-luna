CREATE TABLE IF NOT EXISTS informations (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  identifier INTEGER NOT NULL,
  description VARCHAR,
  module_type_id INTEGER NOT NULL REFERENCES module_types(id),
  information_type_id INTEGER NOT NULL REFERENCES information_type(id)
);