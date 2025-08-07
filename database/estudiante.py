import psycopg2
from pydantic import EmailStr

from models.estudiante import Estudiante
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_estudiante_pg(
        nombres: str,
        apellidos: str,
        correo: EmailStr,
        estado: str,
        usuario_creacion_id: int,
        matricula: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'nombres',
        'apellidos',
        'correo',
        'estado',
        'usuario_creacion_id'
    ]

    values = [
        nombres,
        apellidos,
        correo,
        estado,
        usuario_creacion_id
    ]

    if matricula is not None:
        fields.append('matricula')
        values.append(matricula)

    sql = "insert into estudiante"

    query = formartear_secuencia_insertar_sql(sql, fields)

    query += " returning estudiante_id;"

    results = execute_query(query, values, conn=conexion)

    return next((item['estudianteId'] for item in results), None)


def query_seleccionar_datos_estudiante():
    return '''
           select e.estudiante_id,
                  e.nombres,
                  e.apellidos,
                  e.correo,
                  e.matricula,
                  e.estado,
                  e.fecha_creacion,
                  e.fecha_actualizacion,
                  json_build_object(
                          'usuarioId', uc.usuario_id,
                          'nombre', uc.nombre
                  ) as usuario_creacion,
                  CASE
                      WHEN ua.usuario_id IS NOT NULL THEN
                          json_build_object(
                                  'usuarioId', ua.usuario_id,
                                  'nombre', ua.nombre
                          )
                      ELSE NULL
                      END as usuario_actualizacion
           from estudiante e
                    join usuario uc on e.usuario_creacion_id = uc.usuario_id
                    left join usuario ua on e.usuario_actualizacion_id = ua.usuario_id
           '''


def obtener_estudiante_pg(
        estudiante_id: int | None = None,
        correo: EmailStr | None = None,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = query_seleccionar_datos_estudiante()

    where_exprss = []
    values = []

    if estudiante_id is not None:
        where_exprss.append("e.estudiante_id = %s")
        values.append(estudiante_id)

    if correo is not None:
        where_exprss.append("e.correo = %s")
        values.append(correo)

    if estado is not None:
        where_exprss.append("e.estado = %s")
        values.append(estado)

    if where_exprss:
        sql += " where " + " and ".join(where_exprss)

    sql += " order by e.fecha_creacion desc;"

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    items = [Estudiante(**item) for item in results]

    return items


def actualizar_estudiante_pg(
        estudiante_id: int,
        usuario_actualizacion_id: int,
        nombres: str | None = None,
        apellidos: str | None = None,
        correo: EmailStr | None = None,
        matricula: str | None = None,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = []
    values = []

    # Siempre actualizar el usuario que modificó
    fields.append("usuario_actualizacion_id = %s")
    values.append(usuario_actualizacion_id)

    if nombres is not None:
        fields.append("nombres = %s")
        values.append(nombres)

    if apellidos is not None:
        fields.append("apellidos = %s")
        values.append(apellidos)

    if correo is not None:
        fields.append("correo = %s")
        values.append(correo)

    if matricula is not None:
        fields.append("matricula = %s")
        values.append(matricula)

    if estado is not None:
        fields.append("estado = %s")
        values.append(estado)

    if not fields:
        return None

    values.append(estudiante_id)

    sql = """
          update estudiante
          set fecha_actualizacion = (now() at time zone 'EDT'),
          """

    sql += ", ".join(fields)

    sql += " where estudiante_id = %s"

    sql += " returning estudiante_id;"

    estudiante_actualizado = execute_query(sql, values, conn=conexion)

    if not estudiante_actualizado:
        return None

    return estudiante_actualizado[0]['estudianteId']