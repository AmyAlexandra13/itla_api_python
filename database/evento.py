# database/evento.py

from typing import List
import psycopg2

# Utilidades y constantes compartidas
from shared.utils import execute_query
from shared.constante import Estado

# Modelos para la estructura de datos
from models.evento import Evento
from models.requests.registrar_evento import RegistrarEventoRequest
from models.requests.actualizar_evento import ActualizarEventoRequest

def obtener_evento_pg(
        evento_id: int | None = None,
        estado: str | None = Estado.ACTIVO,
        conexion: psycopg2.extensions.connection | None = None
) -> List[Evento]:
    """
    Obtiene una lista de eventos desde la base de datos, con la opción de filtrar.
    """
    sql = """
          SELECT e.evento_id, \
                 e.nombre, \
                 e.descripcion, \
                 e.fecha_inicio, \
                 e.fecha_fin, \
                 e.estado, \
                 ce.categoria_evento_id, \
                 ce.nombre as categoria_nombre
          FROM evento e
                   JOIN categoria_evento ce ON e.categoria_evento_id = ce.categoria_evento_id
          WHERE 1 = 1 \
          """
    values = []
    if evento_id:
        sql += " AND e.evento_id = %s"
        values.append(evento_id)
    if estado:
        sql += " AND e.estado = %s"
        values.append(estado)

    sql += " ORDER BY e.fecha_inicio DESC;"

    resultado_query = execute_query(sql, values, conn=conexion, fetch_all=True)

    eventos = [Evento.from_dict(row) for row in resultado_query]
    return eventos


def registrar_evento_pg(
        data: RegistrarEventoRequest,
        usuario_creacion_id: int,
        conexion: psycopg2.extensions.connection | None = None
) -> int | None:
    """
    Registra un nuevo evento en la base de datos.
    """
    sql = """
          INSERT INTO evento (nombre, descripcion, fecha_inicio, fecha_fin, categoria_evento_id, estado, fecha_creacion, \
                              usuario_creacion_id)
          VALUES (%s, %s, %s, %s, %s, %s, (now() at time zone 'EDT'), %s) RETURNING evento_id; \
          """
    values = [data.nombre, data.descripcion, data.fecha_inicio, data.fecha_fin, data.categoria_evento_id, Estado.ACTIVO,
              usuario_creacion_id]

    resultado = execute_query(sql, values, conn=conexion)
    return resultado.get('evento_id') if resultado else None


def actualizar_evento_pg(
        evento_id: int,
        data: ActualizarEventoRequest,
        usuario_actualizacion_id: int,
        conexion: psycopg2.extensions.connection | None = None
) -> int | None:
    """
    Actualiza los datos de un evento existente.
    """
    sql = """
          UPDATE evento
          SET nombre                   = %s, \
              descripcion              = %s, \
              fecha_inicio             = %s, \
              fecha_fin                = %s, \
              categoria_evento_id      = %s, \
              fecha_actualizacion      = (now() at time zone 'EDT'), \
              usuario_actualizacion_id = %s
          WHERE evento_id = %s RETURNING evento_id; \
          """
    values = [data.nombre, data.descripcion, data.fecha_inicio, data.fecha_fin, data.categoria_evento_id,
              usuario_actualizacion_id, evento_id]

    resultado = execute_query(sql, values, conn=conexion)
    return resultado.get('evento_id') if resultado else None


def eliminar_evento_pg(
        evento_id: int,
        usuario_actualizacion_id: int,
        conexion: psycopg2.extensions.connection | None = None
) -> int | None:
    """
    Realiza un 'soft delete' de un evento.
    """
    sql = """
          UPDATE evento
          SET estado                   = %s, \
              fecha_actualizacion      = (now() at time zone 'EDT'), \
              usuario_actualizacion_id = %s
          WHERE evento_id = %s RETURNING evento_id; \
          """
    values = [Estado.INACTIVO, usuario_actualizacion_id, evento_id]

    resultado = execute_query(sql, values, conn=conexion)
    return resultado.get('evento_id') if resultado else None