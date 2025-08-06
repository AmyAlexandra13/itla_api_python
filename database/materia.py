import psycopg2

from models.materia import Materia
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_materia_pg(
        nombre: str,
        codigo: str,
        credito: int,
        estado: str,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'nombre',
        'codigo',
        'credito',
        'estado'
    ]

    values = [nombre, codigo, credito, estado]

    sql = "insert into materia"

    query = formartear_secuencia_insertar_sql(sql, fields)

    query += " returning materia_id"

    query += " ;"

    results = execute_query(query, values, conn=conexion)

    return next((item['materiaId'] for item in results), None)


def obtener_materia_pg(
        materia_id: int | None = None,
        estado: str | None = None,
        codigo: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = """
        SELECT materia_id, nombre, codigo, estado, credito, 
               fecha_creacion, fecha_actualizacion
        FROM materia
    """

    conditions = []
    values = []

    if materia_id is not None:
        conditions.append("materia_id = %s")
        values.append(materia_id)

    if estado is not None:
        conditions.append("estado = %s")
        values.append(estado)

    if codigo is not None:
        conditions.append("codigo = %s")
        values.append(codigo)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY materia_id;"

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    items = [Materia(**item) for item in results]

    return items


def actualizar_materia_pg(
        materia_id: int,
        nombre: str | None = None,
        codigo: str | None = None,
        estado: str | None = None,
        credito: int | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = []
    values = []

    if nombre is not None:
        fields.append("nombre = %s")
        values.append(nombre)

    if codigo is not None:
        fields.append("codigo = %s")
        values.append(codigo)

    if estado is not None:
        fields.append("estado = %s")
        values.append(estado)

    if credito is not None:
        fields.append("credito = %s")
        values.append(credito)

    if not fields:
        return None

    values.append(materia_id)

    sql = """
          update materia set fecha_actualizacion = (now() at time zone 'EDT'), 
          """

    sql += ", ".join(fields)

    sql += " where materia_id = %s"

    sql += " returning materia_id"

    sql += " ;"

    materia_actualizada = execute_query(sql, values, conn=conexion)

    if not materia_actualizada:
        return None

    return materia_actualizada[0]['materiaId']


def registrar_programa_academico_materia_pg(
        programa_academico_id: int,
        materia_id: int,
        estado: str,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'programa_academico_id',
        'materia_id',
        'estado'
    ]

    values = [programa_academico_id, materia_id, estado]

    sql = "insert into programa_academico_materia"

    query = formartear_secuencia_insertar_sql(sql, fields)

    query += " returning programa_academico_materia_id"

    query += " ;"

    results = execute_query(query, values, conn=conexion)

    return next((item['programaAcademicoMateriaId'] for item in results), None)


def eliminar_programa_academico_materia_pg(
        materia_id: int,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = "DELETE FROM programa_academico_materia WHERE materia_id = %s;"
    values = [materia_id]

    execute_query(sql, values, conn=conexion)
    return True


def obtener_programa_academico_materia_por_materia_pg(
        materia_id: int,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = """
        SELECT programa_academico_id 
        FROM programa_academico_materia 
        WHERE materia_id = %s AND estado = 'AC'
    """
    values = [materia_id]

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return []

    return [item['programaAcademicoId'] for item in results]
