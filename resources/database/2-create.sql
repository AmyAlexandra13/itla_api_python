create table if not exists rol(
    rol_id bigserial primary key,
    nombre varchar(250) not null,
    estado varchar(2) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,


    constraint rol_estado_ck
        check(estado in ('AC', 'IN'))
);

create table if not exists usuario(
	usuario_id bigserial primary key,
	nombre varchar(250) not null,
	correo varchar(250) not null,
	clave varchar not null,
	estado varchar(2) not null,
    rol_id bigint not null,
	fecha_creacion timestamp not null default (now() at time zone 'EDT'),
	fecha_actualizacion timestamp null,
	
	constraint usuario_estado_ck
		check(estado in ('AC', 'IN')),

    constraint usuario_rol_id_ck
        foreign key (rol_id)
        references rol(rol_id)
        on delete restrict
);


create table if not exists categoria_evento (
    categoria_evento_id bigserial primary key,
    nombre varchar(250) not null,
    estado varchar(2) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    usuario_creacion_id bigint not null,
    fecha_actualizacion timestamp null,
    usuario_actualizacion_id bigint null,

    constraint categoria_evento_usuario_creacion_id_fk
        foreign key(usuario_creacion_id)
        references usuario(usuario_id)
        on delete restrict,

    constraint categoria_evento_usuario_actualizacion_id_fk
        foreign key(usuario_actualizacion_id)
        references usuario(usuario_id)
        on delete restrict,

    constraint categoria_evento_estado_ck
        check(estado in ('AC', 'IN'))
);

create table if not exists evento(
    evento_id bigserial primary key,
    nombre varchar(250) not null,
    descripcion varchar(250) null,
    usuario_creacion_id bigint not null,
    categoria_evento_id bigint not null,
    estado varchar(2) not null,
    fecha_inicio timestamp not null,
    fecha_fin timestamp not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,
    usuario_actualizacion_id bigint null,

    constraint evento_usuario_creacion_id_fk
        foreign key(usuario_creacion_id)
        references usuario(usuario_id)
        on delete restrict,

    constraint evento_usuario_actualizacion_id_fk
        foreign key(usuario_actualizacion_id)
        references usuario(usuario_id)
        on delete restrict,

    constraint evento_estado_ck
        check(estado in ('AC', 'IN')),

    constraint evento_categoria_evento_id_fk
        foreign key(categoria_evento_id)
        references categoria_evento(categoria_evento_id)
        on delete restrict
);



create table if not exists usuario_rol(
    usuario_rol_id bigserial primary key,
    usuario_id bigint not null,
    rol_id bigint not null,
    estado varchar(2) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,

    constraint usuario_rol_usuario_id_fk
        foreign key(usuario_id)
        references usuario(usuario_id)
        on delete restrict,

    constraint usuario_rol_rol_id_fk
        foreign key(rol_id)
        references rol(rol_id)
        on delete restrict,

    constraint usuario_rol_estado_ck
        check(estado in ('AC', 'IN'))
);


create table if not exists editorial(
    editorial_id bigserial primary key,
    nombre varchar(250) not null,
    estado varchar(2) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,


    constraint editorial_estado_ck
        check(estado in ('AC', 'IN'))
);


create table if not exists libro(
    libro_id bigserial primary key,
    editorial_id bigint not null,
    titulo varchar(250) not null,
    sipnosis varchar(250) null,
    year_publicacion smallint null,
    archivo_url varchar(250) null,
    imagen_url varchar(250) null,
    estado varchar(2) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,


    constraint libro_editorial_id_fk
        foreign key(editorial_id)
        references editorial(editorial_id)
        on delete restrict,

    constraint libro_estado_ck
        check(estado in ('AC', 'IN'))
);
-- Tabla principal
CREATE TABLE IF NOT EXISTS editoriales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de autores
CREATE TABLE IF NOT EXISTS autores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100),
    biografia TEXT,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de libros
CREATE TABLE IF NOT EXISTS libros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    anio_publicacion INT,
    editorial_id INT REFERENCES editoriales(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla puente: muchos libros pueden tener muchos autores
CREATE TABLE IF NOT EXISTS libro_autor (
    id SERIAL PRIMARY KEY,
    libro_id INT REFERENCES libros(id) ON DELETE CASCADE,
    autor_id INT REFERENCES autores(id) ON DELETE CASCADE
);