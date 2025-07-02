import psycopg2
from pydantic import EmailStr

from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_usuario_pg(
        nombre: str,
        correo: EmailStr,
        clave: str,
        estado: str,
        rol_id: int,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'nombre',
        'correo',
        'clave',
        'estado',
        'rol_id'
    ]

    values = [nombre, correo, clave, estado, rol_id]

    sql = "insert into usuario"

    query = formartear_secuencia_insertar_sql(sql, fields)

    query += " returning usuario_id"

    query += " ;"

    results = execute_query(query, values, conn=conexion)

    return next((item['usuarioId'] for item in results), None)


def obtener_usuario_pg(
        correo: EmailStr,
        conexion: psycopg2.extensions.connection | None = None
):

    query = "select * from usuario where correo = %s;"

    results = execute_query(query, [correo], conn=conexion)

    return next((item for item in results), None)


def buscar_rol_usuario_pg(
        usuario_id: int,
        rol_id: int,
        conexion: psycopg2.extensions.connection | None = None
):
    query = """
            select 
                u.usuario_id,
                u.nombre,
                u.correo,
                u.estado
            from usuario u
            join rol r on u.rol_id = r.rol_id
            where u.estado = 'AC' and r.estado = 'AC'
                and u.usuario_id = %s and r.rol_id = %s;
    """

    values = [usuario_id, rol_id]

    results = execute_query(query, values, conn=conexion)

    return next((item for item in results), None)





