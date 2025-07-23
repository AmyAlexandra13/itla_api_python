from database.connection import get_connection
from models.requests.registrar_editorial import RegistrarEditorialRequest
from models.requests.actualizar_editorial import ActualizarEditorialRequest
from models.response.editorial import EditorialResponse
from fastapi import HTTPException

def registrar_editorial_pg(
        nombre: str,
        estado: str,
        conexion=None
):
    sql = """
        INSERT INTO editorial (nombre, estado)
        VALUES (%s, %s)
        RETURNING editorial_id
    """
    conn = conexion or get_connection()
    cur = conn.cursor()
    cur.execute(sql, [nombre, estado])
    editorial_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    if conexion is None:
        conn.close()
    return editorial_id

def query_seleccionar_datos_editorial():
    return '''
        SELECT editorial_id,
               nombre,
               estado,
               fecha_creacion,
               fecha_actualizacion
        FROM editorial
    '''

def obtener_editorial_pg(
        editorial_id: int = None,
        estado: str = None,
        conexion=None
):
    sql = query_seleccionar_datos_editorial()
    where_exprss = []
    values = []

    if editorial_id is not None:
        where_exprss.append("editorial_id = %s")
        values.append(editorial_id)
    if estado is not None:
        where_exprss.append("estado = %s")
        values.append(estado)

    if where_exprss:
        sql += " WHERE " + " AND ".join(where_exprss)

    sql += " ORDER BY editorial_id DESC;"

    conn = conexion or get_connection()
    cur = conn.cursor()
    cur.execute(sql, values)
    rows = cur.fetchall()
    cur.close()
    if conexion is None:
        conn.close()
    items = [EditorialResponse(
        editorial_id=row[0],
        nombre=row[1],
        estado=row[2],
        fecha_creacion=row[3],
        fecha_actualizacion=row[4]
    ) for row in rows]
    return items

def actualizar_editorial_pg(
        editorial_id: int,
        nombre: str = None,
        estado: str = None,
        conexion=None
):
    fields = []
    values = []

    if nombre is not None:
        fields.append("nombre = %s")
        values.append(nombre)
    if estado is not None:
        fields.append("estado = %s")
        values.append(estado)

    # actualiza fecha_actualizacion cada vez que se edita
    fields.append("fecha_actualizacion = (now() at time zone 'EDT')")

    if not fields:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    values.append(editorial_id)

    sql = f"""
        UPDATE editorial
        SET {', '.join(fields)}
        WHERE editorial_id = %s
        RETURNING editorial_id, nombre, estado, fecha_creacion, fecha_actualizacion;
    """

    conn = conexion or get_connection()
    cur = conn.cursor()
    cur.execute(sql, values)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    if conexion is None:
        conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    return EditorialResponse(
        editorial_id=row[0],
        nombre=row[1],
        estado=row[2],
        fecha_creacion=row[3],
        fecha_actualizacion=row[4]
    )

def eliminar_editorial_pg(
        editorial_id: int,
        conexion=None
):
    sql = "DELETE FROM editorial WHERE editorial_id = %s;"
    conn = conexion or get_connection()
    cur = conn.cursor()
    cur.execute(sql, [editorial_id])
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    if conexion is None:
        conn.close()
    return deleted
