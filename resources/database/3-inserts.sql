insert into rol
	(nombre, estado)
values
    ('Administrador', 'AC'),
    ('Usuario', 'AC'),
    ('Cliente', 'AC');

-- Insertar nuevas carreras de tecnología
INSERT INTO programa_academico (nombre, estado, periodo_academico) VALUES
('Desarrollo de Software', 'AC', '2024-2025'),
('Ciberseguridad', 'AC', '2024-2025'),
('Redes de la Información', 'AC', '2024-2025');

-- Insertar materias específicas para estas carreras
INSERT INTO materia (nombre, codigo, estado, credito) VALUES
-- Materias para Desarrollo de Software
('Programación III', 'PROG003', 'AC', 4),
('Desarrollo Web Frontend', 'WEBF001', 'AC', 4),
('Desarrollo Web Backend', 'WEBB001', 'AC', 4),
('Metodologías Ágiles', 'AGIL001', 'AC', 3),
('Arquitectura de Software', 'ARQS001', 'AC', 4),
('Testing y QA', 'TEST001', 'AC', 3),
('DevOps y CI/CD', 'DEVO001', 'AC', 3),
('Desarrollo Mobile', 'MOBI001', 'AC', 4),

-- Materias para Ciberseguridad
('Fundamentos de Ciberseguridad', 'CIBF001', 'AC', 3),
('Criptografía', 'CRIP001', 'AC', 4),
('Ethical Hacking', 'HACK001', 'AC', 4),
('Forense Digital', 'FORE001', 'AC', 4),
('Seguridad en Redes', 'SEGR001', 'AC', 4),
('Gestión de Riesgos', 'RIES001', 'AC', 3),
('Compliance y Auditoría', 'COMP001', 'AC', 3),
('Incident Response', 'INCI001', 'AC', 3),

-- Materias para Redes de la Información
('Fundamentos de Redes', 'REDF001', 'AC', 4),
('Configuración de Routers', 'ROUT001', 'AC', 4),
('Configuración de Switches', 'SWIT001', 'AC', 4),
('Protocolos de Red', 'PROT001', 'AC', 3),
('Administración de Servidores', 'SERV001', 'AC', 4),
('Virtualización', 'VIRT001', 'AC', 3),
('Cloud Computing', 'CLOU001', 'AC', 4),
('Monitoreo de Redes', 'MONI001', 'AC', 3),

-- Materias transversales para tecnología
('Inglés Técnico', 'INGT001', 'AC', 2),
('Ética Profesional', 'ETIC001', 'AC', 2),
('Gestión de Proyectos TI', 'GETI001', 'AC', 3);

-- Obtener los IDs de los programas académicos recién insertados
-- (Asumiendo que son los IDs 5, 6, 7 si ya existían 4 programas anteriormente)

-- Asignar materias a Desarrollo de Software (programa_academico_id = 5)
INSERT INTO programa_academico_materia (programa_academico_id, materia_id, estado) VALUES
-- Materias básicas compartidas
(5, 1, 'AC'),  -- Programación I
(5, 2, 'AC'),  -- Matemáticas I
(5, 6, 'AC'),  -- Estadística
(5, 7, 'AC'),  -- Base de Datos
(5, 8, 'AC'),  -- Cálculo Diferencial

-- Materias específicas de Desarrollo de Software
(5, 9, 'AC'),  -- Programación III
(5, 10, 'AC'), -- Desarrollo Web Frontend
(5, 11, 'AC'), -- Desarrollo Web Backend
(5, 12, 'AC'), -- Metodologías Ágiles
(5, 13, 'AC'), -- Arquitectura de Software
(5, 14, 'AC'), -- Testing y QA
(5, 15, 'AC'), -- DevOps y CI/CD
(5, 16, 'AC'), -- Desarrollo Mobile

-- Materias transversales
(5, 33, 'AC'), -- Inglés Técnico
(5, 34, 'AC'), -- Ética Profesional
(5, 35, 'AC'), -- Gestión de Proyectos TI

-- Asignar materias a Ciberseguridad (programa_academico_id = 6)
INSERT INTO programa_academico_materia (programa_academico_id, materia_id, estado) VALUES
-- Materias básicas compartidas
(6, 1, 'AC'),  -- Programación I
(6, 2, 'AC'),  -- Matemáticas I
(6, 6, 'AC'),  -- Estadística
(6, 7, 'AC'),  -- Base de Datos

-- Materias específicas de Ciberseguridad
(6, 17, 'AC'), -- Fundamentos de Ciberseguridad
(6, 18, 'AC'), -- Criptografía
(6, 19, 'AC'), -- Ethical Hacking
(6, 20, 'AC'), -- Forense Digital
(6, 21, 'AC'), -- Seguridad en Redes
(6, 22, 'AC'), -- Gestión de Riesgos
(6, 23, 'AC'), -- Compliance y Auditoría
(6, 24, 'AC'), -- Incident Response

-- Materias de redes (útiles para ciberseguridad)
(6, 25, 'AC'), -- Fundamentos de Redes
(6, 29, 'AC'), -- Protocolos de Red

-- Materias transversales
(6, 33, 'AC'), -- Inglés Técnico
(6, 34, 'AC'), -- Ética Profesional
(6, 35, 'AC'), -- Gestión de Proyectos TI

-- Asignar materias a Redes de la Información (programa_academico_id = 7)
INSERT INTO programa_academico_materia (programa_academico_id, materia_id, estado) VALUES
-- Materias básicas compartidas
(7, 2, 'AC'),  -- Matemáticas I
(7, 3, 'AC'),  -- Física I
(7, 6, 'AC'),  -- Estadística

-- Materias específicas de Redes
(7, 25, 'AC'), -- Fundamentos de Redes
(7, 26, 'AC'), -- Configuración de Routers
(7, 27, 'AC'), -- Configuración de Switches
(7, 28, 'AC'), -- Protocolos de Red
(7, 29, 'AC'), -- Administración de Servidores
(7, 30, 'AC'), -- Virtualización
(7, 31, 'AC'), -- Cloud Computing
(7, 32, 'AC'), -- Monitoreo de Redes

-- Materias de seguridad (importantes para redes)
(7, 17, 'AC'), -- Fundamentos de Ciberseguridad
(7, 21, 'AC'), -- Seguridad en Redes

-- Programación básica
(7, 1, 'AC'),  -- Programación I

-- Materias transversales
(7, 33, 'AC'), -- Inglés Técnico
(7, 34, 'AC'), -- Ética Profesional
(7, 35, 'AC'); -- Gestión de Proyectos TI