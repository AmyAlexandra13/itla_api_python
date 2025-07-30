import psycopg2
from models.editorial import Editorial
from shared.utils import execute_query

def registrar_editorial_pg(nombre: str, estado: str,
                            conexion: psycopg2.extensions.connection | None = None):
    sql = """
        insert into editorial (nombre, estado)
        VALUES (%s, %s)
        RETURNING editorial_id;
    """
    values = [nombre, estado]
    result = execute_query(sql, values, conn=conexion)
    return next((item['editorialId'] for item in result), None)


def obtener_editorial_pg(editorial_id: int | None = None,
                          estado: str | None = None,
                          conexion: psycopg2.extensions.connection | None = None):
    sql = """
        SELECT editorial_id, nombre, estado, fecha_creacion, fecha_actualizacion
        FROM editorial
    """
    conditions = []
    values = []

    if editorial_id is not None:
        conditions.append("editorial_id = %s")
        values.append(editorial_id)

    if estado is not None:
        conditions.append("estado = %s")
        values.append(estado)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY editorial_id;"

    result = execute_query(sql, values, conn=conexion)
    return [Editorial(**item) for item in result] if result else None


def actualizar_editorial_pg(editorial_id: int,
                             nombre: str | None = None,
                             estado: str | None = None,
                             conexion: psycopg2.extensions.connection | None = None):
    updates = []
    values = []

    if nombre is not None:
        updates.append("nombre = %s")
        values.append(nombre)

    if estado is not None:
        updates.append("estado = %s")
        values.append(estado)

    if not updates:
        return None

    sql = f"""
        UPDATE editorial
        SET {", ".join(updates)},
            fecha_actualizacion = (now() at time zone 'EDT')
        WHERE editorial_id = %s
        RETURNING editorial_id;
    """

    values.append(editorial_id)
    result = execute_query(sql, values, conn=conexion)
    return next((item['editorialId'] for item in result), None)
