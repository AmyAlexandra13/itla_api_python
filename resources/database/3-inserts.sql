insert into rol
	(nombre, estado)
values
    ('Administrador', 'AC'),
    ('Usuario', 'AC'),
    ('Cliente', 'AC');

-- Insertar un usuario administrador para la API de UNICDA
INSERT INTO usuario (usuario_id, rol_id, nombre, correo, clave, estado, fecha_creacion)
VALUES
(1, 1, 'unicda', 'unicda@unicda.com', '$2b$12$9pOcGGbuVQIxQPGsiPGs4Oec9KtKItEyAjFI.Pu/aS6AyFEHhN4T.', 'AC', CURRENT_TIMESTAMP);

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

-- Inserción de categorías de eventos
INSERT INTO categoria_evento (nombre, estado, usuario_creacion_id)
VALUES
    ('Desarrollo de Software', 'AC', 1),       -- ID 1
    ('Redes y Telecomunicaciones', 'AC', 1),   -- ID 2
    ('Seguridad Informática', 'AC', 1),        -- ID 3
    ('Profesorado de Inglés', 'AC', 1),        -- ID 4
    ('Profesorado de Otras Lenguas', 'AC', 1); -- ID 5

-- Desarrollo de Software (ID 1)
INSERT INTO evento (nombre, descripcion, usuario_creacion_id, categoria_evento_id, estado, fecha_inicio, fecha_fin)
VALUES
('Taller de Programación en Java', 'Introducción a conceptos modernos de Java y Spring Boot.', 1, 1, 'AC', '2025-01-15 09:00', '2025-01-15 12:00'),
('Hackathon Universitario', 'Competencia intensiva de desarrollo de software en 24 horas.', 1, 1, 'AC', '2025-02-10 08:00', '2025-02-10 20:00'),
('Workshop de Inteligencia Artificial', 'Aplicaciones de IA en la industria actual.', 1, 1, 'AC', '2025-03-12 14:00', '2025-03-12 17:00'),
('Seminario de Arquitectura de Software', 'Buenas prácticas para escalabilidad de sistemas.', 1, 1, 'AC', '2025-04-20 10:00', '2025-04-20 13:00'),
('Taller de Desarrollo Móvil con Flutter', 'Aplicaciones multiplataforma Android/iOS.', 1, 1, 'AC', '2025-05-05 09:00', '2025-05-05 12:00'),
('Conferencia sobre Cloud Computing', 'Servicios y despliegues en AWS y Azure.', 1, 1, 'AC', '2025-06-15 15:00', '2025-06-15 18:00'),
('Taller de Bases de Datos PostgreSQL', 'Modelado y optimización de consultas.', 1, 1, 'AC', '2025-08-10 09:00', '2025-08-10 12:00'),
('Workshop de React y Next.js', 'Creación de aplicaciones web modernas.', 1, 1, 'AC', '2025-09-12 14:00', '2025-09-12 17:00'),
('Curso de Automatización con Python', 'Automatización de procesos administrativos.', 1, 1, 'AC', '2025-10-18 09:00', '2025-10-18 12:00'),
('Foro de Innovación Tecnológica', 'Tendencias y retos en el desarrollo de software.', 1, 1, 'AC', '2025-11-20 10:00', '2025-11-20 13:00');

-- Redes y Telecomunicaciones (ID 2)
INSERT INTO evento (nombre, descripcion, usuario_creacion_id, categoria_evento_id, estado, fecha_inicio, fecha_fin)
VALUES
('Seminario de Redes Cisco', 'Configuración avanzada de routers y switches.', 1, 2, 'AC', '2025-01-25 09:00', '2025-01-25 12:00'),
('Taller de Administración de Servidores Linux', 'Instalación y configuración de servicios.', 1, 2, 'AC', '2025-02-18 14:00', '2025-02-18 17:00'),
('Workshop de Redes Inalámbricas', 'Optimización de redes Wi-Fi en entornos corporativos.', 1, 2, 'AC', '2025-03-25 09:00', '2025-03-25 12:00'),
('Conferencia sobre 5G y Futuro de Telecomunicaciones', 'Impacto del 5G en la industria.', 1, 2, 'AC', '2025-04-28 10:00', '2025-04-28 13:00'),
('Taller de Seguridad en Redes', 'Protección contra ataques comunes.', 1, 2, 'AC', '2025-06-05 14:00', '2025-06-05 17:00'),
('Seminario de Cableado Estructurado', 'Normas y buenas prácticas.', 1, 2, 'AC', '2025-07-15 09:00', '2025-07-15 12:00'),
('Práctica de Configuración de VPNs', 'Conexiones seguras para empresas.', 1, 2, 'AC', '2025-09-05 09:00', '2025-09-05 12:00'),
('Workshop de Virtualización con VMware', 'Implementación de entornos virtualizados.', 1, 2, 'AC', '2025-10-08 14:00', '2025-10-08 17:00'),
('Taller de Monitoreo de Redes', 'Uso de herramientas como Zabbix y Nagios.', 1, 2, 'AC', '2025-12-03 09:00', '2025-12-03 12:00');

-- Seguridad Informática (ID 3)
INSERT INTO evento (nombre, descripcion, usuario_creacion_id, categoria_evento_id, estado, fecha_inicio, fecha_fin)
VALUES
('Taller de Pentesting Básico', 'Introducción a pruebas de penetración.', 1, 3, 'AC', '2025-01-12 09:00', '2025-01-12 12:00'),
('Conferencia de Ciberseguridad Empresarial', 'Protección de datos y continuidad de negocio.', 1, 3, 'AC', '2025-02-20 10:00', '2025-02-20 13:00'),
('Curso de Análisis Forense Digital', 'Técnicas para recuperar y analizar evidencias.', 1, 3, 'AC', '2025-03-15 14:00', '2025-03-15 17:00'),
('Seminario de Malware y Ransomware', 'Detección y mitigación de amenazas.', 1, 3, 'AC', '2025-04-25 09:00', '2025-04-25 12:00'),
('Workshop de Seguridad en Aplicaciones Web', 'Prácticas OWASP y pruebas de seguridad.', 1, 3, 'AC', '2025-06-12 14:00', '2025-06-12 17:00'),
('Taller de Criptografía Aplicada', 'Implementación de cifrado y firma digital.', 1, 3, 'AC', '2025-07-18 09:00', '2025-07-18 12:00'),
('Simulación de Incidentes de Seguridad', 'Respuesta ante ciberataques reales.', 1, 3, 'AC', '2025-09-15 10:00', '2025-09-15 13:00'),
('Curso de Seguridad en la Nube', 'Prácticas seguras en AWS y Azure.', 1, 3, 'AC', '2025-10-25 09:00', '2025-10-25 12:00'),
('Foro de Ética Hacker', 'Debate sobre el hacking ético.', 1, 3, 'AC', '2025-12-10 14:00', '2025-12-10 17:00');

-- Profesorado de Inglés (ID 4)
INSERT INTO evento (nombre, descripcion, usuario_creacion_id, categoria_evento_id, estado, fecha_inicio, fecha_fin)
VALUES
('Workshop de Pronunciación Avanzada', 'Mejora de acento y fluidez.', 1, 4, 'AC', '2025-01-20 09:00', '2025-01-20 12:00'),
('Curso de Enseñanza de Inglés con Tecnología', 'Uso de apps y plataformas interactivas.', 1, 4, 'AC', '2025-02-28 10:00', '2025-02-28 13:00'),
('Seminario de Metodologías de Enseñanza', 'Métodos modernos y efectivos.', 1, 4, 'AC', '2025-03-22 14:00', '2025-03-22 17:00'),
('Taller de Inglés para Negocios', 'Vocabulario y prácticas empresariales.', 1, 4, 'AC', '2025-04-18 09:00', '2025-04-18 12:00'),
('Conferencia sobre Evaluación Lingüística', 'Pruebas estandarizadas y diagnósticas.', 1, 4, 'AC', '2025-05-28 14:00', '2025-05-28 17:00'),
('Taller de Recursos Didácticos Digitales', 'Diseño y aplicación en clases.', 1, 4, 'AC', '2025-07-10 09:00', '2025-07-10 12:00'),
('Workshop de Conversación Intensiva', 'Práctica guiada con hablantes nativos.', 1, 4, 'AC', '2025-09-20 09:00', '2025-09-20 12:00'),
('Seminario de Traducción e Interpretación', 'Técnicas para traducción simultánea.', 1, 4, 'AC', '2025-10-12 14:00', '2025-10-12 17:00'),
('Foro de Cultura Angloparlante', 'Costumbres y cultura de países de habla inglesa.', 1, 4, 'AC', '2025-11-28 10:00', '2025-11-28 13:00');

-- Profesorado de Otras Lenguas (ID 5)
INSERT INTO evento (nombre, descripcion, usuario_creacion_id, categoria_evento_id, estado, fecha_inicio, fecha_fin)
VALUES
('Taller de Francés Conversacional', 'Mejora de la expresión oral.', 1, 5, 'AC', '2025-02-05 09:00', '2025-02-05 12:00'),
('Workshop de Enseñanza de Español para Extranjeros', 'Metodologías adaptadas.', 1, 5, 'AC', '2025-03-18 14:00', '2025-03-18 17:00'),
('Seminario de Lengua Portuguesa', 'Gramática y vocabulario básico.', 1, 5, 'AC', '2025-04-22 09:00', '2025-04-22 12:00'),
('Taller de Cultura Japonesa', 'Idioma, costumbres y tradiciones.', 1, 5, 'AC', '2025-05-15 10:00', '2025-05-15 13:00'),
('Curso de Italiano para Principiantes', 'Introducción al idioma.', 1, 5, 'AC', '2025-07-25 09:00', '2025-07-25 12:00'),
('Seminario de Lenguas Indígenas Caribeñas', 'Preservación y enseñanza.', 1, 5, 'AC', '2025-09-10 14:00', '2025-09-10 17:00'),
('Workshop de Alemán Básico', 'Pronunciación y frases comunes.', 1, 5, 'AC', '2025-10-28 09:00', '2025-10-28 12:00'),
('Foro de Multilingüismo', 'Importancia del aprendizaje de varios idiomas.', 1, 5, 'AC', '2025-12-15 10:00', '2025-12-15 13:00');
