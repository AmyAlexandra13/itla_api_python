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


INSERT INTO programa_academico_materia (programa_academico_id, materia_id, estado) VALUES
(1, 1, 'AC'),   -- Programación I
(1, 2, 'AC'),   -- Matemáticas I
(1, 4, 'AC'),   -- Estadística
(1, 5, 'AC'),   -- Base de Datos
(1, 6, 'AC'),   -- Cálculo Diferencial
(1, 7, 'AC'),   -- Programación III
(1, 8, 'AC'),   -- Desarrollo Web Frontend
(1, 9, 'AC'),   -- Desarrollo Web Backend
(1, 10, 'AC'),  -- Metodologías Ágiles
(1, 11, 'AC'),  -- Arquitectura de Software
(1, 12, 'AC'),  -- Testing y QA
(1, 13, 'AC'),  -- DevOps y CI/CD
(1, 14, 'AC'),  -- Desarrollo Mobile
(1, 31, 'AC'),  -- Inglés Técnico
(1, 32, 'AC'),  -- Ética Profesional
(1, 33, 'AC'),  -- Gestión de Proyectos TI
(2, 1, 'AC'),   -- Programación I
(2, 2, 'AC'),   -- Matemáticas I
(2, 4, 'AC'),   -- Estadística
(2, 5, 'AC'),   -- Base de Datos
(2, 15, 'AC'),  -- Fundamentos de Ciberseguridad
(2, 16, 'AC'),  -- Criptografía
(2, 17, 'AC'),  -- Ethical Hacking
(2, 18, 'AC'),  -- Forense Digital
(2, 19, 'AC'),  -- Seguridad en Redes
(2, 20, 'AC'),  -- Gestión de Riesgos
(2, 21, 'AC'),  -- Compliance y Auditoría
(2, 22, 'AC'),  -- Incident Response
(2, 23, 'AC'),  -- Fundamentos de Redes
(2, 26, 'AC'),  -- Protocolos de Red
(2, 31, 'AC'),  -- Inglés Técnico
(2, 32, 'AC'),  -- Ética Profesional
(2, 33, 'AC'),  -- Gestión
(3, 2, 'AC'),   -- Matemáticas I
(3, 3, 'AC'),   -- Física I
(3, 4, 'AC'),   -- Estadística
(3, 23, 'AC'),  -- Fundamentos de Redes
(3, 24, 'AC'),  -- Configuración de Routers
(3, 25, 'AC'),  -- Configuración de Switches
(3, 26, 'AC'),  -- Protocolos de Red
(3, 27, 'AC'),  -- Administración de Servidores
(3, 28, 'AC'),  -- Virtualización
(3, 29, 'AC'),  -- Cloud Computing
(3, 30, 'AC'),  -- Monitoreo de Redes
(3, 15, 'AC'),  -- Fundamentos de Ciberseguridad
(3, 19, 'AC'),  -- Seguridad en Redes
(3, 1, 'AC'),   -- Programación I
(3, 31, 'AC'),  -- Inglés Técnico
(3, 32, 'AC'),  -- Ética Profesional
(3, 33, 'AC');  -- Gesti