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