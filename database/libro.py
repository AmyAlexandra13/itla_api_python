from datetime import datetime
import psycopg2

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
