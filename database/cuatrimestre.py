import logging
from typing import Optional, List, Dict, Any
import psycopg2
from models.cuatrimestre import Cuatrimestre
from models.paginacion import Paginacion
from shared.utils import execute_query, formartear_secuencia_insertar_sql


def registrar_cuatrimestre_pg(
        periodo: str,
        anio: int,
        estado: str,
        conexion: psycopg2.extensions.connection
) -> Optional[int]:
    try:
        sql = "INSERT INTO cuatrimestre"
        fields = ["periodo", "anio", "estado"]
        values = [periodo, anio, estado]

        query = formartear_secuencia_insertar_sql(sql, fields)
        query += " RETURNING cuatrimestre_id"

        cursor = conexion.cursor()
        cursor.execute(query, values)
        cuatrimestre_id = cursor.fetchone()[0]
        cursor.close()

        return cuatrimestre_id

    except Exception as e:
        logging.error(f"Error al registrar cuatrimestre: {str(e)}")
        raise e


def obtener_cuatrimestre_pg(
        cuatrimestre_id: Optional[int] = None,
        periodo: Optional[str] = None,
        anio: Optional[int] = None,
        estado: Optional[str] = None,
        numero_pagina: Optional[int] = None,
        limite: Optional[int] = None,
        conexion: psycopg2.extensions.connection = None
) -> Optional[Dict[str, Any] | List[Cuatrimestre]]:
    try:
        sql = """
            SELECT 
                c.cuatrimestre_id,
                c.periodo,
                c.anio,
                c.estado,
                c.fecha_creacion,
                c.fecha_actualizacion
            FROM cuatrimestre c
            WHERE 1=1
        """

        values = []

        if cuatrimestre_id is not None:
            sql += " AND c.cuatrimestre_id = %s"
            values.append(cuatrimestre_id)

        if periodo is not None:
            sql += " AND c.periodo = %s"
            values.append(periodo)

        if anio is not None:
            sql += " AND c.anio = %s"
            values.append(anio)

        if estado is not None:
            sql += " AND c.estado = %s"
            values.append(estado)

        sql += " ORDER BY c.anio DESC, c.periodo"

        # Si no hay paginación, devolver lista directamente
        if numero_pagina is None or limite is None:
            resultado = execute_query(sql, values, conexion)
            if not resultado:
                return None

            cuatrimestres = [Cuatrimestre(**row) for row in resultado]
            return cuatrimestres

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
            FROM cuatrimestre c
            WHERE 1=1
        """

        if cuatrimestre_id is not None:
            sql_count += " AND c.cuatrimestre_id = %s"

        if periodo is not None:
            sql_count += " AND c.periodo = %s"

        if anio is not None:
            sql_count += " AND c.anio = %s"

        if estado is not None:
            sql_count += " AND c.estado = %s"

        count_resultado = execute_query(sql_count, values, conexion)
        total = count_resultado[0]['total'] if count_resultado else 0

        total_paginas = (total + limite - 1) // limite

        cuatrimestres = [Cuatrimestre(**row) for row in resultado]

        paginacion = Paginacion(
            total=total,
            numeroPagina=numero_pagina,
            limite=limite,
            totalPaginas=total_paginas
        )

        return {
            "cuatrimestres": cuatrimestres,
            "paginacion": paginacion
        }

    except Exception as e:
        logging.error(f"Error al obtener cuatrimestres: {str(e)}")
        raise e


def actualizar_cuatrimestre_pg(
        cuatrimestre_id: int,
        periodo: Optional[str] = None,
        anio: Optional[int] = None,
        estado: Optional[str] = None,
        conexion: psycopg2.extensions.connection = None
) -> bool:
    try:
        # Construir campos dinámicamente
        campos = []
        values = []

        if periodo is not None:
            campos.append("periodo = %s")
            values.append(periodo)

        if anio is not None:
            campos.append("anio = %s")
            values.append(anio)

        if estado is not None:
            campos.append("estado = %s")
            values.append(estado)

        if not campos:
            return False

        campos.append("fecha_actualizacion = NOW()")
        values.append(cuatrimestre_id)

        sql = f"""
            UPDATE cuatrimestre 
            SET {', '.join(campos)}
            WHERE cuatrimestre_id = %s
        """

        cursor = conexion.cursor()
        cursor.execute(sql, values)
        rows_affected = cursor.rowcount
        cursor.close()

        return rows_affected > 0

    except Exception as e:
        logging.error(f"Error al actualizar cuatrimestre: {str(e)}")
        raise e