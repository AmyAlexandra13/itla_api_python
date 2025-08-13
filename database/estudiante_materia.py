import logging
from typing import Optional, List, Dict, Any
from decimal import Decimal
import psycopg2
from models.estudiante_materia import EstudianteMateria, MateriaOut, EstudianteOut, CuatrimestreOut
from models.paginacion import Paginacion
from shared.utils import execute_query, formartear_secuencia_insertar_sql


def registrar_estudiante_materia_pg(
        estudiante_id: int,
        materia_id: int,
        cuatrimestre_id: int,
        estado: str,
        conexion: psycopg2.extensions.connection,
        calificacion: Decimal | None = None,

) -> Optional[int]:
    try:
        sql = "INSERT INTO estudiante_materia"
        fields = ["estudiante_id", "materia_id", "cuatrimestre_id", "estado", "calificacion"]
        values = [estudiante_id, materia_id, cuatrimestre_id, estado, calificacion]

        query = formartear_secuencia_insertar_sql(sql, fields)
        query += " RETURNING estudiante_materia_id"

        cursor = conexion.cursor()
        cursor.execute(query, values)
        estudiante_materia_id = cursor.fetchone()[0]
        cursor.close()

        return estudiante_materia_id

    except Exception as e:
        logging.error(f"Error al registrar estudiante-materia: {str(e)}")
        raise e


def obtener_estudiante_materia_pg(
        estudiante_materia_id: Optional[int] = None,
        estudiante_id: Optional[int] = None,
        materia_id: Optional[int] = None,
        cuatrimestre_id: Optional[int] = None,
        estado: Optional[str] = None,
        numero_pagina: Optional[int] = None,
        limite: Optional[int] = None,
        conexion: psycopg2.extensions.connection = None
) -> Optional[Dict[str, Any] | List[EstudianteMateria]]:
    try:
        sql = """
            SELECT 
                em.estudiante_materia_id,
                em.estudiante_id,
                em.materia_id,
                em.cuatrimestre_id,
                em.estado,
                em.calificacion,
                em.fecha_creacion,
                em.fecha_actualizacion,
                e.nombres as estudiante_nombres,
                e.apellidos as estudiante_apellidos,
                m.nombre as materia_nombre,
                m.codigo as materia_codigo,
                c.periodo as cuatrimestre_periodo,
                c.anio as cuatrimestre_anio
            FROM estudiante_materia em
            INNER JOIN estudiante e ON em.estudiante_id = e.estudiante_id
            INNER JOIN materia m ON em.materia_id = m.materia_id
            INNER JOIN cuatrimestre c ON em.cuatrimestre_id = c.cuatrimestre_id
            WHERE 1=1
        """

        values = []

        if estudiante_materia_id is not None:
            sql += " AND em.estudiante_materia_id = %s"
            values.append(estudiante_materia_id)

        if estudiante_id is not None:
            sql += " AND em.estudiante_id = %s"
            values.append(estudiante_id)

        if materia_id is not None:
            sql += " AND em.materia_id = %s"
            values.append(materia_id)

        if cuatrimestre_id is not None:
            sql += " AND em.cuatrimestre_id = %s"
            values.append(cuatrimestre_id)

        if estado is not None:
            sql += " AND em.estado = %s"
            values.append(estado)

        sql += " ORDER BY c.anio DESC, c.periodo, e.apellidos, e.nombres, m.nombre"

        # Si no hay paginación, devolver lista directamente
        if numero_pagina is None or limite is None:
            resultado = execute_query(sql, values, conexion)
            if not resultado:
                return None

            estudiante_materias = []
            for row in resultado:
                estudiante_materia = EstudianteMateria(
                    estudianteMateriaId=row['estudianteMateriaId'],
                    estudianteId=row['estudianteId'],
                    materiaId=row['materiaId'],
                    cuatrimestreId=row['cuatrimestreId'],
                    estado=row['estado'],
                    calificacion=row['calificacion'],
                    fechaCreacion=row['fechaCreacion'],
                    fechaActualizacion=row['fechaActualizacion'],
                    estudiante=EstudianteOut(
                        estudianteId=row['estudianteId'],
                        nombres=row['estudianteNombres'],
                        apellidos=row['estudianteApellidos']
                ),
                    materia=MateriaOut(
                        materiaId=row['materiaId'],
                        nombre=row['materiaNombre'],
                        codigo=row['materiaCodigo']
                ),
                    cuatrimestre=CuatrimestreOut(
                        cuatrimestreId=row['cuatrimestreId'],
                        periodo=row['cuatrimestrePeriodo'],
                        anio=row['cuatrimestreAnio']
                )
                )
                estudiante_materias.append(estudiante_materia)

            return estudiante_materias

        # Con paginación
        offset = (numero_pagina - 1) * limite
        sql_paginado = sql + f" LIMIT %s OFFSET %s"
        values_paginado = values + [limite, offset]

        resultado = execute_query(sql_paginado, values_paginado, conexion)

        if not resultado:
            return None

        # Contar total de registros
        sql_count = """
            SELECT COUNT(*) as total
            FROM estudiante_materia em
            INNER JOIN estudiante e ON em.estudiante_id = e.estudiante_id
            INNER JOIN materia m ON em.materia_id = m.materia_id
            INNER JOIN cuatrimestre c ON em.cuatrimestre_id = c.cuatrimestre_id
            WHERE 1=1
        """

        if estudiante_materia_id is not None:
            sql_count += " AND em.estudiante_materia_id = %s"

        if estudiante_id is not None:
            sql_count += " AND em.estudiante_id = %s"

        if materia_id is not None:
            sql_count += " AND em.materia_id = %s"

        if cuatrimestre_id is not None:
            sql_count += " AND em.cuatrimestre_id = %s"

        if estado is not None:
            sql_count += " AND em.estado = %s"

        count_resultado = execute_query(sql_count, values, conexion)
        total = count_resultado[0]['total'] if count_resultado else 0

        total_paginas = (total + limite - 1) // limite

        estudiante_materias = []
        for row in resultado:
            estudiante_materia = EstudianteMateria(
                estudianteMateriaId=row['estudianteMateriaId'],
                estudianteId=row['estudianteId'],
                materiaId=row['materiaId'],
                cuatrimestreId=row['cuatrimestreId'],
                estado=row['estado'],
                calificacion=row['calificacion'],
                fechaCreacion=row['fechaCreacion'],
                fechaActualizacion=row['fechaActualizacion'],
                estudiante=EstudianteOut(
                    estudianteId=row['estudianteId'],
                    nombres=row['estudianteNombres'],
                    apellidos=row['estudianteApellidos']
                ),
                materia=MateriaOut(
                    materiaId=row['materiaId'],
                    nombre=row['materiaNombre'],
                    codigo=row['materiaCodigo']
                ),
                cuatrimestre=CuatrimestreOut(
                    cuatrimestreId=row['cuatrimestreId'],
                    periodo=row['cuatrimestrePeriodo'],
                    anio=row['cuatrimestreAnio']
                )
            )
            estudiante_materias.append(estudiante_materia)

        paginacion = Paginacion(
            total=total,
            numeroPagina=numero_pagina,
            limite=limite,
            totalPaginas=total_paginas
        )

        return {
            "estudiantesMaterias": estudiante_materias,
            "paginacion": paginacion
        }

    except Exception as e:
        logging.error(f"Error al obtener estudiante-materia: {str(e)}")
        raise e


def actualizar_estudiante_materia_pg(
        estudiante_materia_id: int,
        estado: Optional[str] = None,
        calificacion: Optional[Decimal] = None,
        conexion: psycopg2.extensions.connection = None
) -> bool:
    try:
        # Construir campos dinámicamente
        campos = []
        values = []

        if estado is not None:
            campos.append("estado = %s")
            values.append(estado)

        if calificacion is not None:
            campos.append("calificacion = %s")
            values.append(calificacion)

        if not campos:
            return False

        campos.append("fecha_actualizacion = (now() at time zone 'EDT')")
        values.append(estudiante_materia_id)

        sql = f"""
            UPDATE estudiante_materia 
            SET {', '.join(campos)}
            WHERE estudiante_materia_id = %s
        """

        cursor = conexion.cursor()
        cursor.execute(sql, values)
        rows_affected = cursor.rowcount
        cursor.close()

        return rows_affected > 0

    except Exception as e:
        logging.error(f"Error al actualizar estudiante-materia: {str(e)}")
        raise e


def verificar_estudiante_materia_existente_pg(
        estudiante_id: int,
        materia_id: int,
        cuatrimestre_id: int,
        conexion: psycopg2.extensions.connection
) -> bool:
    """
    Verifica si ya existe un registro de estudiante-materia para el cuatrimestre dado
    """
    try:
        sql = """
            SELECT 1 
            FROM estudiante_materia 
            WHERE estudiante_id = %s 
            AND materia_id = %s 
            AND cuatrimestre_id = %s
        """

        resultado = execute_query(sql, [estudiante_id, materia_id, cuatrimestre_id], conexion)

        return resultado is not None and len(resultado) > 0

    except Exception as e:
        logging.error(f"Error al verificar estudiante-materia existente: {str(e)}")
        raise e