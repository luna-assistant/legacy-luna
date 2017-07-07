INSERT INTO roles (id, name, display_name)
VALUES
  (1, 'admin', 'Administrador'),
  (2, 'comum', 'Comum'),
  (3, 'associado', 'Associado')
ON CONFLICT (id) DO UPDATE
SET
  name = EXCLUDED.name,
  display_name = EXCLUDED.display_name;
