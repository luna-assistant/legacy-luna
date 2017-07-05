INSERT INTO command_types (id, description)
VALUES
  (1, 'Acionamento'),
  (2, 'Parametrização'),
  (3, 'Leitura')
ON CONFLICT (id) DO UPDATE 
SET 
  description = EXCLUDED.description;