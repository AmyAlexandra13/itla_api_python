import math
from typing import Dict, Any, List

import psycopg2
from pydantic import EmailStr

from models.estudiante import Estudiante
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_estudiante_pg(
        nombres: str,
        apellidos: str,
        correo: EmailStr,
        estado: str,
        cedula: str,
        telefono: str,
        usuario_creacion_id: int,
        matricula: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'nombres',
        'apellidos',
        'correo',
        'estado',
        'cedula',
        'telefono',
        'usuario_creacion_id'
    ]

    values = [
        nombres,
        apellidos,
        correo,
        estado,
        cedula,
        telefono,
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
                  e.cedula,
                  e.telefono,
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


def query_contar_estudiantes():
    return '''
           select count(*) as total
           from estudiante e
                    join usuario uc on e.usuario_creacion_id = uc.usuario_id
                    left join usuario ua on e.usuario_actualizacion_id = ua.usuario_id
           '''


def obtener_estudiante_pg(
        estudiante_id: int | None = None,
        correo: str | None = None,
        estado: str | None = None,
        matricula: str | None = None,
        numero_pagina: int | None = None,
        limite: int | None = None,
        conexion: psycopg2.extensions.connection | None = None
) -> Dict[str, Any] | List[Estudiante] | None:
    # Construir las condiciones WHERE
    where_exprss = []
    values = []

    if estudiante_id is not None:
        where_exprss.append("e.estudiante_id = %s")
        values.append(estudiante_id)

    if correo is not None:
        where_exprss.append("upper(e.correo) = %s")
        values.append(correo.upper())

    if estado is not None:
        where_exprss.append("e.estado = %s")
        values.append(estado)

    if matricula is not None:
        where_exprss.append("e.matricula = %s")
        values.append(matricula)

    where_clause = ""
    if where_exprss:
        where_clause = " where " + " and ".join(where_exprss)

    # Si se solicita paginación
    if numero_pagina is not None and limite is not None:
        # Validar parámetros de paginación
        if numero_pagina < 1:
            numero_pagina = 1
        if limite < 1:
            limite = 10

        # Contar total de registros
        sql_count = query_contar_estudiantes() + where_clause + ";"
        count_results = execute_query(sql_count, values, conn=conexion)

        if not count_results:
            return {
                "estudiantes": [],
                "paginacion": {
                    "total": 0,
                    "numeroPagina": numero_pagina,
                    "limite": limite,
                    "totalPaginas": 0
                }
            }

        total_registros = count_results[0]['total']
        total_paginas = math.ceil(total_registros / limite)

        # Si la página solicitada es mayor al total de páginas, devolver la última página
        if numero_pagina > total_paginas and total_paginas > 0:
            numero_pagina = total_paginas

        # Construir query con paginación
        offset = (numero_pagina - 1) * limite
        sql = query_seleccionar_datos_estudiante()
        sql += where_clause
        sql += " order by e.fecha_creacion desc"
        sql += f" limit {limite} offset {offset};"

        results = execute_query(sql, values, conn=conexion)

        estudiantes = []
        if results:
            estudiantes = [Estudiante(**item) for item in results]

        return {
            "estudiantes": estudiantes,
            "paginacion": {
                "total": total_registros,
                "numeroPagina": numero_pagina,
                "limite": limite,
                "totalPaginas": total_paginas
            }
        }

    # Sin paginación - comportamiento original
    else:
        sql = query_seleccionar_datos_estudiante()
        sql += where_clause
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
        cedula: str | None = None,
        telefono: str | None = None,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = []
    values = []

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

    if cedula is not None:
        fields.append("cedula = %s")
        values.append(cedula)

    if telefono is not None:
        fields.append("telefono = %s")
        values.append(telefono)

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
