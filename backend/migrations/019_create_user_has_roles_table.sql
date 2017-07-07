CREATE TABLE IF NOT EXISTS user_has_roles (
  user_id INTEGER REFERENCES users(id),
  role_id INTEGER REFERENCES roles(id),
  PRIMARY KEY (user_id, role_id)
);
