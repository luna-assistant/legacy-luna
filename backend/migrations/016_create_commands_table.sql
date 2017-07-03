CREATE TABLE IF NOT EXISTS commands (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  identifier INTEGER NOT NULL,
  description VARCHAR,
  module_type_id INTEGER NOT NULL REFERENCES module_types(id),
  command_type_id INTEGER NOT NULL REFERENCES command_types(id)
);