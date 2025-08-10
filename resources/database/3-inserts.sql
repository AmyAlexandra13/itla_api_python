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
