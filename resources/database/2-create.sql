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
    usuario_creacion_id bigint not null,
    cantidad_disponible bigint not null,
    sipnosis varchar(250) null,
    year_publicacion smallint null,
    archivo_url varchar(250) null,
    imagen_url varchar null,
    content bytea NOT NULL,
    estado varchar(2) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,
    usuario_actualizacion_id bigint null,

    constraint libro_usuario_creacion_id_fk
        foreign key(usuario_creacion_id)
        references usuario(usuario_id)
        on delete restrict,

    constraint libro_usuario_actualizacion_id_fk
        foreign key(usuario_actualizacion_id)
        references usuario(usuario_id)
        on delete restrict,


    constraint libro_editorial_id_fk
        foreign key(editorial_id)
        references editorial(editorial_id)
        on delete restrict,

    constraint libro_estado_ck
        check(estado in ('AC', 'IN'))
);


create table if not exists programa_academico(
    programa_academico_id bigserial primary key,
    nombre varchar(250) not null,
    estado varchar(2) not null,
    periodo_academico varchar(9) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,

    constraint programa_academico_estado_ck
        check(estado in ('AC', 'IN'))
);

create table if not exists materia(
    materia_id bigserial primary key,
    nombre varchar(250) not null,
    codigo varchar(20) not null,
    estado varchar(2) not null,
    credito bigint not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,

    constraint materia_estado_ck
        check(estado in ('AC', 'IN'))
);

create table if not exists programa_academico_materia(
    programa_academico_materia_id bigserial primary key,
    programa_academico_id bigint not null,
    materia_id bigint not null,
    estado varchar(2) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,

    constraint programa_academico_materia_estado_ck
        check(estado in ('AC', 'IN')),

    constraint programa_academico_materia_programa_academico_id_fk
        foreign key(programa_academico_id)

        references programa_academico(programa_academico_id)
        on delete restrict,

    constraint programa_academico_materia_materia_id_fk
        foreign key(materia_id)
        references materia(materia_id)
        on delete restrict,

    constraint programa_academico_materia_id_programa_academico_id_uk
        unique(programa_academico_id, materia_id)
);

create table if not exists estudiante(
    estudiante_id bigserial primary key not null,
    nombres varchar (250) not null,
    apellidos varchar (250) not null,
    correo varchar(50) not null,
    matricula varchar (20) null,
    estado varchar(30) not null,
    usuario_creacion_id bigint not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    usuario_actualizacion_id bigint null,
    fecha_actualizacion timestamp null,

    constraint estudiante_estado_ck
        check(estado in ('REGISTRADO', 'PENDIENTE_DOCUMENTO', 'PENDIENTE_RESPUESTA', 'ACEPTADO', 'RECHAZADO', 'ACTIVO', 'GRADUADO')),

    constraint estudiante_usuario_creacion_id_fk
        foreign key(usuario_creacion_id)
        references usuario(usuario_id)
        on delete restrict,

    constraint estudiante_usuario_actualizacion_id_fk
        foreign key(usuario_actualizacion_id)
        references usuario(usuario_id)
        on delete restrict,

    constraint estudiante_correo_uk
        unique(correo)
)

create table if not exists estudiante_documento(
    estudiante_documento_id bigserial primary key not null,
    estudiante_id bigint not null,
    tipo_documento varchar(20) not null,
    content bytea NOT NULL,
    estado varchar(20) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,

    constraint estudiante_documento_estado_ck
        check(estado in ('PENDIENTE', 'VALIDO', 'RECHAZADO')),

    constraint estudiante_documento_estudiante_id_fk
        foreign key(estudiante_id)
        references estudiante(estudiante_id)
        on delete restrict,

    constraint estudiante_documento_tipo_documento_ck
        check(tipo_documento in ('CEDULA', 'ACTA_NACIMIENTO', 'RECORD_ESCUELA')),

    constraint estudiante_documento_estudiante_id_tipo_documento_uk
        unique(estudiante_id, tipo_documento)
);

create table if not exists estudiante_programa_academico(
    estudiante_programa_academico_id bigserial primary key not null,
    estudiante_id bigint not null,
    programa_academico_id bigint not null,
    estado varchar(10) not null,
    fecha_creacion timestamp not null default (now() at time zone 'EDT'),
    fecha_actualizacion timestamp null,

    constraint estudiante_programa_academico_estado_ck
        check(estado in ('AC', 'IN', 'EN_CURSO', 'TERMINADO')),

    constraint estudiante_programa_academico_estudiante_id_fk
        foreign key(estudiante_id)
        references estudiante(estudiante_id)
        on delete restrict,

    constraint estudiante_programa_academico_programa_academico_id_fk
        foreign key (programa_academico_id)
        references programa_academico(programa_academico_id)
        on delete restrict
);


