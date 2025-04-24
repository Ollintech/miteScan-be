insert into accesses (name, description) 
values 
('Admin', 'Acesso de administrador com permissões completas'),
('User', 'Acesso de usuário com permissões limitadas');

insert into companies (name, cnpj) 
values 
('MiteScan Ltda.', 12345678000195),
('BeeTech Innovations', 98765432000158);

-- Supondo que o `access_id` refere-se a `Admin` (id=1) e `company_id` refere-se a `MiteScan Ltda.` (id=1)
insert into users (name, email, password_hash, last_login, status, access_id, company_id) 
values 
('Carlos Silva', 'carlos@mitescan.com', 'hashed_password_example', '2025-04-02 12:00:00', true, 1, 1),
('Maria Oliveira', 'maria@beetech.com', 'hashed_password_example', '2025-04-02 14:30:00', true, 2, 2);

-- Supondo que o `user_id` refere-se a `Carlos Silva` (id=1)
insert into bee_types (name, description, user_id) 
values 
('Africanized Honeybee', 'A raça de abelha africana', 1),
('European Honeybee', 'A tradicional abelha europeia', 1);

-- Supondo que `user_id` é `Carlos Silva` (id=1) e `bee_type_id` é `Africanized Honeybee` (id=1)
insert into hives (user_id, bee_type_id, location_lat, location_lng, size, humidity, temperature) 
values 
(1, 1, -23.55052, -46.633308, 50, 60.5, 28.0),
(1, 2, -22.903539, -43.209587, 40, 58.3, 25.5);

-- Supondo que `hive_id` é `1` e `user_id` é `Carlos Silva` (id=1)
insert into hive_analysis (hive_id, user_id, image_path, varroa_detected, detection_confidence, created_at) 
values 
(1, 1, '/images/hive_1_analysis.jpg', false, 0.95, '2025-04-02 12:30:00'),
(2, 1, '/images/hive_2_analysis.jpg', true, 0.85, '2025-04-02 15:00:00');

-- Supondo que `user_id` é `Carlos Silva` (id=1) e `analysis_id` é `1` (primeiro registro de `hive_analysis`)
insert into analysis_backups (user_id, file_path, analysis_id) 
values 
(1, '/backups/analysis_1_backup.zip', 1),
(1, '/backups/analysis_2_backup.zip', 2);
