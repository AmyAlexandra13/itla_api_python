from datetime import datetime

import psycopg2

from models.libro import Libro
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_libro_pg(
        editorial_id: int,
        titulo: str,
        estado: str,
        content: bytes,
        usuario_creacion_id: int,
        cantidad_disponible: int,
        sipnosis: str | None = None,
        year_publicacion: int | None = None,
        archivo_url: str | None = None,
        imagen_url: str | None = None,
        fecha_actualizacion: datetime | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'editorial_id',
        'titulo',
        'estado',
        'content',
        'usuario_creacion_id',
        'cantidad_disponible',
        'sipnosis',
        'year_publicacion',
        'archivo_url',
        'imagen_url',
        'fecha_actualizacion'
    ]

    values = [
        editorial_id,
        titulo,
        estado,
        psycopg2.Binary(content),
        usuario_creacion_id,
        cantidad_disponible,
        sipnosis,
        year_publicacion,
        archivo_url,
        imagen_url,
        fecha_actualizacion
    ]

    # Quitar campos nulos para evitar problemas en el insert dinámico
    fields_cleaned = []

    values_cleaned = []

    for f, v in zip(fields, values):
        if v is not None:
            fields_cleaned.append(f)

            values_cleaned.append(v)

    sql = "insert into libro"

    query = formartear_secuencia_insertar_sql(sql, fields_cleaned)

    query += " returning libro_id;"

    results = execute_query(query, values_cleaned, conn=conexion)

    return next((item['libroId'] for item in results), None)


def query_seleccionar_datos_libro():
    return '''
           SELECT l.libro_id,
                  l.titulo,
                  l.sipnosis,
                  l.year_publicacion,
                  l.archivo_url,
                  l.imagen_url,
                  l.estado,
                  to_char(l.fecha_creacion, 'DD-MM-YYYY HH24:MI:SS')      AS fecha_creacion,
                  to_char(l.fecha_actualizacion, 'DD-MM-YYYY HH24:MI:SS') AS fecha_actualizacion,

                  json_build_object(
                          'usuarioId', uc.usuario_id,
                          'nombre', uc.nombre
                  )                                                       AS usuario_creacion,

                  CASE
                      WHEN ua.usuario_id IS NOT NULL THEN
                          json_build_object(
                                  'usuarioId', ua.usuario_id,
                                  'nombre', ua.nombre
                          )
                      ELSE NULL
                      END                                                 AS usuario_actualizacion,

                  json_build_object(
                          'editorialId', e.editorial_id,
                          'nombre', e.nombre
                  )                                                       AS editorial

           FROM libro l
                    JOIN usuario uc ON l.usuario_creacion_id = uc.usuario_id
                    LEFT JOIN usuario ua ON l.usuario_actualizacion_id = ua.usuario_id
                    JOIN editorial e ON l.editorial_id = e.editorial_id

           '''


def obtener_libros_pg(
        libro_id: int | None = None,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = query_seleccionar_datos_libro()

    where_exprss = []
    values = []

    if libro_id is not None:
        where_exprss.append("l.libro_id = %s")
        values.append(libro_id)

    if estado is not None:
        where_exprss.append("l.estado = %s")
        values.append(estado)

    if where_exprss:
        sql += " WHERE " + " AND ".join(where_exprss)

    sql += " ORDER BY l.fecha_creacion DESC;"

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    items = [Libro(**item) for item in results]

    return items
