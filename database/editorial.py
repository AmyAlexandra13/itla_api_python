from database.connection import get_connection
from models.requests.registrar_editorial import RegistrarEditorialRequest
from models.requests.actualizar_editorial import ActualizarEditorialRequest
from models.response.editorial import EditorialResponse
from fastapi import HTTPException

def crear_editorial(data: RegistrarEditorialRequest) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO editoriales (nombre, correo, telefono, direccion, estado)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (data.nombre, data.correo, data.telefono, data.direccion, data.estado))
    editorial_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return editorial_id

def listar_editoriales() -> list[EditorialResponse]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, correo, telefono, direccion, estado, fecha_creacion
        FROM editoriales
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        EditorialResponse(
            id=row[0],
            nombre=row[1],
            correo=row[2],
            telefono=row[3],
            direccion=row[4],
            estado=row[5],
            fecha_creacion=row[6]
        )
        for row in rows
    ]

def obtener_editorial(editorial_id: int) -> EditorialResponse:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, correo, telefono, direccion, estado, fecha_creacion
        FROM editoriales
        WHERE id = %s
    """, (editorial_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    return EditorialResponse(
        id=row[0],
        nombre=row[1],
        correo=row[2],
        telefono=row[3],
        direccion=row[4],
        estado=row[5],
        fecha_creacion=row[6]
    )

def actualizar_editorial(editorial_id: int, data: ActualizarEditorialRequest) -> EditorialResponse:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE editoriales
        SET nombre = %s,
            correo = %s,
            telefono = %s,
            direccion = %s,
            estado = %s
        WHERE id = %s
        RETURNING id, nombre, correo, telefono, direccion, estado, fecha_creacion
    """, (data.nombre, data.correo, data.telefono, data.direccion, data.estado, editorial_id))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="No se pudo actualizar la editorial")

    return EditorialResponse(
        id=row[0],
        nombre=row[1],
        correo=row[2],
        telefono=row[3],
        direccion=row[4],
        estado=row[5],
        fecha_creacion=row[6]
    )

def eliminar_editorial(editorial_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM editoriales WHERE id = %s", (editorial_id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return deleted

print("✅ Cargando archivo editorial.py")
