import psycopg2

from models.categoria_evento import CategoriaEvento
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_cateogoria_evento_pg(
        nombre: str,
        usuario_creacion_id: int,
        estado: str,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'nombre',
        'estado',
        'usuario_creacion_id'
    ]

    values = [nombre, estado, usuario_creacion_id]

    sql = "insert into categoria_evento"

    query = formartear_secuencia_insertar_sql(sql, fields)

    query += " returning categoria_evento_id"

    query += " ;"

    results = execute_query(query, values, conn=conexion)

    return next((item['categoriaEventoId'] for item in results), None)


def query_seleccionar_datos_categoria_evento():
    return '''
        select
            ce.categoria_evento_id,
            ce.nombre,
            ce.estado,
            to_char(ce.fecha_creacion, 'DD-MM-YYYY') fecha_creacion,
            json_build_object(
                'usuarioId', u.usuario_id,
                'nombre', u.nombre
            ) usuario
        from categoria_evento ce
        join usuario u on ce.usuario_creacion_id = u.usuario_id
    '''


def obtener_categoria_evento_pg(
        categoria_evento_id: int | None = None,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = query_seleccionar_datos_categoria_evento()

    where_exprss = []
    values = []


    if categoria_evento_id is not None:
        where_exprss.append("ce.categoria_evento_id = %s")
        values.append(categoria_evento_id)


    if estado is not None:
        where_exprss.append("ce.estado = %s")
        values.append(estado)


    if where_exprss:
        sql += " where " + " and ".join(where_exprss)

    sql += " ;"


    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    items = [CategoriaEvento(**item) for item in results]

    return items


def actualizar_categoria_evento_pg(
        categoria_evento_id: int,
        nombre: str | None = None,
        estado: str | None = None,
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

    values.append(categoria_evento_id)

    sql = """
          update categoria_evento set fecha_actualizacion = (now() at time zone 'EDT'), 
          """

    sql += ", ".join(fields)

    sql += " where categoria_evento_id = %s"

    sql += " returning categoria_evento_id"

    sql += " ;"

    categoria_evento_actualizado = execute_query(sql, values, conn=conexion)

    if not categoria_evento_actualizado:
        return None

    return categoria_evento_actualizado[0]['categoriaEventoId']