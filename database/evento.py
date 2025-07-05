from datetime import datetime

import psycopg2

from models.evento import Evento
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_evento_pg(
        nombre: str,
        usuario_creacion_id: int,
        categoria_evento_id: int,
        estado: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        descripcion: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'nombre',
        'usuario_creacion_id',
        'categoria_evento_id',
        'estado',
        'fecha_inicio',
        'fecha_fin',
        'descripcion'
    ]

    values = [
        nombre,
        usuario_creacion_id,
        categoria_evento_id,
        estado,
        fecha_inicio,
        fecha_fin,
        descripcion
    ]

    sql = "insert into evento"

    query = formartear_secuencia_insertar_sql(sql, fields)

    query += " returning evento_id"

    query += " ;"

    results = execute_query(query, values, conn=conexion)

    return next((item['eventoId'] for item in results), None)


def query_seleccionar_datos_evento():
    return '''
           select e.evento_id,
                  e.nombre,
                  e.descripcion,
                  e.estado,
                  e.fecha_creacion,
                  json_build_object(
                          'usuarioId', u.usuario_id,
                          'nombre', u.nombre
                  )                                       usuario,
                  json_build_object(
                          'categoriaEventoId', ce.categoria_evento_id,
                          'nombre', ce.nombre
                  )                                       categoria_evento,
                    e.fecha_inicio,
                    e.fecha_fin,
                    e.fecha_actualizacion,
                    e.usuario_actualizacion_id
           from evento e
                    join usuario u on e.usuario_creacion_id = u.usuario_id
                    join categoria_evento ce on e.categoria_evento_id = ce.categoria_evento_id \
           '''


def obtener_evento_pg(
        evento_id: int | None = None,
        categoria_evento_id: int | None = None,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = query_seleccionar_datos_evento()

    where_exprss = []
    values = []

    if evento_id is not None:
        where_exprss.append("e.evento_id = %s")
        values.append(evento_id)

    if categoria_evento_id is not None:
        where_exprss.append("e.categoria_evento_id = %s")
        values.append(categoria_evento_id)

    if estado is not None:
        where_exprss.append("e.estado = %s")
        values.append(estado)

    if where_exprss:
        sql += " where " + " and ".join(where_exprss)

    sql += " ;"

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    items = [Evento(**item) for item in results]

    return items


def actualizar_evento_pg(
        evento_id: int,
        usuario_actualizacion_id: int,
        nombre: str | None = None,
        categoria_evento_id: int | None = None,
        estado: str | None = None,
        fecha_inicio: datetime | None = None,
        fecha_fin: datetime | None = None,
        descripcion: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = []
    values = []

    fields.append("usuario_actualizacion_id = %s")
    values.append(usuario_actualizacion_id)

    if nombre is not None:
        fields.append("nombre = %s")
        values.append(nombre)

    if categoria_evento_id is not None:
        fields.append("categoria_evento_id = %s")
        values.append(categoria_evento_id)

    if estado is not None:
        fields.append("estado = %s")
        values.append(estado)

    if fecha_inicio is not None:
        fields.append("fecha_inicio = %s")
        values.append(fecha_inicio)

    if fecha_fin is not None:
        fields.append("fecha_fin = %s")
        values.append(fecha_fin)

    if descripcion is not None:
        fields.append("descripcion = %s")
        values.append(descripcion)

    values.append(evento_id)

    sql = """
          update evento
          set fecha_actualizacion = (now() at time zone 'EDT'),
          """

    sql += ", ".join(fields)

    sql += " where evento_id = %s"

    sql += " returning evento_id"

    sql += " ;"

    evento_actualizado = execute_query(sql, values, conn=conexion)

    if not evento_actualizado:
        return None

    return evento_actualizado[0]['eventoId']
