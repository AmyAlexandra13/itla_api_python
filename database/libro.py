from datetime import datetime

import psycopg2

from models.libro import Libro
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_libro_pg(
        editorial_id: int,
        titulo: str,
        estado: str,
        content: bytes,
        imagen_url: str,
        usuario_creacion_id: int,
        cantidad_disponible: int,
        sipnosis: str | None = None,
        year_publicacion: int | None = None,
        archivo_url: str | None = None,
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
                  l.cantidad_disponible,
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
        titulo: str | None = None,
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

    if titulo:
        where_exprss.append("upper(l.titulo) ilike upper(%s)")
        values.append(f"%{titulo}%")


    if where_exprss:
        sql += " WHERE " + " AND ".join(where_exprss)

    sql += " ORDER BY l.fecha_creacion DESC;"

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    items = [Libro(**item) for item in results]

    return items


def obtener_content_libro(
        libro_id: int,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = '''
        SELECT content
        FROM libro
        WHERE libro_id = %s;
    '''

    values = [libro_id]

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    return results[0]['content']


def actualizar_libro_pg(
        libro_id: int,
        usuario_actualizacion_id: int,
        editorial_id: int | None = None,
        titulo: str | None = None,
        estado: str | None = None,
        cantidad_disponible: int | None = None,
        sipnosis: str | None = None,
        year_publicacion: int | None = None,
        archivo_url: str | None = None,
        imagen_url: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = []
    values = []

    # Siempre actualizar el usuario que modificó
    fields.append("usuario_actualizacion_id = %s")
    values.append(usuario_actualizacion_id)

    if editorial_id is not None:
        fields.append("editorial_id = %s")
        values.append(editorial_id)

    if titulo is not None:
        fields.append("titulo = %s")
        values.append(titulo)

    if estado is not None:
        fields.append("estado = %s")
        values.append(estado)

    if cantidad_disponible is not None:
        fields.append("cantidad_disponible = %s")
        values.append(cantidad_disponible)

    if sipnosis is not None:
        fields.append("sipnosis = %s")
        values.append(sipnosis)

    if year_publicacion is not None:
        fields.append("year_publicacion = %s")
        values.append(year_publicacion)

    if archivo_url is not None:
        fields.append("archivo_url = %s")
        values.append(archivo_url)

    if imagen_url is not None:
        fields.append("imagen_url = %s")
        values.append(imagen_url)

    values.append(libro_id)

    sql = """
          update libro
          set fecha_actualizacion = (now() at time zone 'EDT'),
          """

    sql += ", ".join(fields)

    sql += " where libro_id = %s"

    sql += " returning libro_id"

    sql += " ;"

    libro_actualizado = execute_query(sql, values, conn=conexion)

    if not libro_actualizado:
        return None

    return libro_actualizado[0]['libroId']
