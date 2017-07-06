INSERT INTO roles (id, name, verbose_name)
VALUES
  (1, 'admin', 'Administrador'),
  (2, 'comum', 'Comum'),
  (3, 'associado', 'Associado')
ON CONFLICT (id) DO UPDATE
SET
  name = EXCLUDED.name,
  verbose_name = EXCLUDED.verbose_name;
