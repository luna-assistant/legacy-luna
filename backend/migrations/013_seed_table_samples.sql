BEGIN;

INSERT INTO users (id, username, password) VALUES

(1, 'superusuario', '$2b$04$jOZB6m2q327qqgfy6oIMcuowrF6Gf9t0RKxifMLbIkV1ZCTCQU.8m'),
(2, 'chicobentojr', '$2b$04$SUyYK5hkDpOPY1t5G1dbG.GUS3aQZeG4PE03QBB5PKzj2jLffjZxC'),
(3, 'felipemfp', '$2b$04$SUyYK5hkDpOPY1t5G1dbG.GUS3aQZeG4PE03QBB5PKzj2jLffjZxC'),
(4, 'yuricosta', '$2b$04$SUyYK5hkDpOPY1t5G1dbG.GUS3aQZeG4PE03QBB5PKzj2jLffjZxC'),
(5, 'dayannemorato', '$2b$04$SUyYK5hkDpOPY1t5G1dbG.GUS3aQZeG4PE03QBB5PKzj2jLffjZxC'),
(6, 'diellyviana', '$2b$04$SUyYK5hkDpOPY1t5G1dbG.GUS3aQZeG4PE03QBB5PKzj2jLffjZxC'),
(7, 'felipebarbosa', '$2b$04$SUyYK5hkDpOPY1t5G1dbG.GUS3aQZeG4PE03QBB5PKzj2jLffjZxC')

ON CONFLICT (id) DO NOTHING;

INSERT INTO people(name, cpf, birth, user_id) VALUES

('Superusuário', '76298205853', '1980-01-01', 1),
('Francisco Bento', '75457985113', '1980-01-01', 2),
('Felipe Pontes', '58937991357', '1980-01-01', 3),
('Yuri Costa', '64444368691', '1980-01-01', 4),
('Dayanne Morato', '26839756866', '1980-01-01', 5),
('Dielly Viana', '46369858935', '1980-01-01', 6),
('Felipe Barbosa', '58372827427', '1980-01-01', 7)

ON CONFLICT (id) DO NOTHING;

COMMIT;
