import psycopg2
from models.programa_academico import ProgramaAcademico
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_programa_academico_pg(
        nombre: str,
        periodo_academico: str,
        estado: str,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'nombre',
        'periodo_academico',
        'estado'
    ]

    values = [nombre, periodo_academico, estado]

    sql = "insert into programa_academico"

    query = formartear_secuencia_insertar_sql(sql, fields)

    query += " returning programa_academico_id"

    query += " ;"

    results = execute_query(query, values, conn=conexion)

    return next((item['programaAcademicoId'] for item in results), None)


def obtener_programa_academico_pg(
        programa_academico_id: int | None = None,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = """
        SELECT programa_academico_id, nombre, estado, periodo_academico, 
               fecha_creacion, fecha_actualizacion
        FROM programa_academico
    """

    conditions = []
    values = []

    if programa_academico_id is not None:
        conditions.append("programa_academico_id = %s")
        values.append(programa_academico_id)

    if estado is not None:
        conditions.append("estado = %s")
        values.append(estado)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY programa_academico_id;"

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    items = [ProgramaAcademico(**item) for item in results]

    return items


def actualizar_programa_academico_pg(
        programa_academico_id: int,
        nombre: str | None = None,
        estado: str | None = None,
        periodo_academico: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = []
    values = []

    if nombre is not None:
        fields.append("nombre = %s")
        values.append(nombre)

    if estado is not None:
        fields.append("estado = %s")
        values.append(estado)

    if periodo_academico is not None:
        fields.append("periodo_academico = %s")
        values.append(periodo_academico)

    if not fields:
        return None

    values.append(programa_academico_id)

    sql = """
          update programa_academico set fecha_actualizacion = (now() at time zone 'EDT'), 
          """

    sql += ", ".join(fields)

    sql += " where programa_academico_id = %s"

    sql += " returning programa_academico_id"

    sql += " ;"

    programa_academico_actualizado = execute_query(sql, values, conn=conexion)

    if not programa_academico_actualizado:
        return None

    return programa_academico_actualizado[0]['programaAcademicoId']