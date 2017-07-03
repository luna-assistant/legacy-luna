INSERT INTO information_types (id, description)
VALUES
  (1, 'Saída Digital'),
  (2, 'Saída Analógica'),
  (3, 'Entrada Digital'),
  (4, 'Entrada Analógica'),
  (5, 'Parâmetro')
ON CONFLICT (id) DO UPDATE 
SET 
  description = EXCLUDED.description;