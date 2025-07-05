import logging
from typing import List

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path, Query

from database.categoria_evento import obtener_categoria_evento_pg
from database.connection import get_connection
from database.evento import registrar_evento_pg, obtener_evento_pg, actualizar_evento_pg
from models.evento import Evento
from models.generico import ResponseData, ResponseList
from models.requests.actualizar_evento import ActualizarEventoRequest
from models.requests.registrar_evento import RegistrarEventoRequest
from shared.constante import Estado, Rol
from shared.permission import get_current_user
from shared.utils import validar_fechas

router = APIRouter(prefix="/evento", tags=["Evento"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarEvento', status_code=status.HTTP_201_CREATED)
def registrar_evento(request: RegistrarEventoRequest = Body(),
                     current_user: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):
    conexion = get_connection()

    try:

        usuario_id = current_user['usuarioId']

        fechas_validas_dict = validar_fechas(request.fechaInicio, request.fechaFin)

        if not fechas_validas_dict['valido']:
            logging.exception("Las fechas inicio y fin del evento son invalidas")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Las fechas inicio y fin del evento son invalidas'
            )

        evento_id = registrar_evento_pg(
            nombre=request.nombre,
            usuario_creacion_id=usuario_id,
            estado=Estado.ACTIVO,
            categoria_evento_id=request.categoriaEventoId,
            descripcion=request.descripcion,
            fecha_inicio=request.fechaInicio,
            fecha_fin=request.fechaFin,
            conexion=conexion
        )

        conexion.commit()

        return ResponseData[int](data=evento_id)

    except HTTPException as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e.detail)


    except Exception as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


    finally:
        conexion.close()


@router.get("/",
            responses={status.HTTP_200_OK: {"model": ResponseList[List[Evento]]}},
            summary='obtenerEvento', status_code=status.HTTP_200_OK)
def buscar_evento(_: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):
    conexion = get_connection()

    try:

        eventos = obtener_evento_pg(
            conexion=conexion
        )

        if not eventos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron eventos'
            )

        conexion.commit()

        return ResponseList(data=eventos)

    except HTTPException as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e.detail)


    except Exception as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


    finally:
        conexion.close()


@router.get("/{eventoId}",
            responses={status.HTTP_200_OK: {"model": ResponseData[Evento]}},
            summary='obtenerEventoPorId', status_code=status.HTTP_200_OK)
def buscar_evento_id(evento_id: int = Path(alias='eventoId', description='Id del evento'),
                     _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
                     estado: str | None = Query(None, min_length=2, max_length=2, pattern="^(IN|AC)$")):
    conexion = get_connection()

    try:

        eventos = obtener_evento_pg(
            evento_id=evento_id,
            estado=estado,
            conexion=conexion
        )

        if not eventos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el evento'
            )

        categoria_evento = eventos[0]

        conexion.commit()

        return ResponseData(data=categoria_evento)

    except HTTPException as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e.detail)


    except Exception as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


    finally:
        conexion.close()


@router.patch("/actualizar",
              summary='actualizarEvento', status_code=status.HTTP_204_NO_CONTENT)
def actualizar_evento(request: ActualizarEventoRequest = Body(),
                      current_user: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):
    conexion = get_connection()

    try:

        categoria_evento_id = request.categoriaEventoId

        usuario_id = current_user['usuarioId']

        evento_id = request.eventoId

        eventos = obtener_evento_pg(
            evento_id=evento_id,
            conexion=conexion
        )

        if not eventos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el evento para actualizar'
            )

        evento = eventos[0]

        categorias_eventos = obtener_categoria_evento_pg(
            categoria_evento_id=categoria_evento_id,
            estado=Estado.ACTIVO,
            conexion=conexion
        )

        if not categorias_eventos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se encontró la categoria del evento activo para actualizar'
            )

        fecha_inicio_validar = request.fechaInicio if request.fechaInicio else evento.fechaInicio

        fecha_fin_validar = request.fechaFin if request.fechaFin else evento.fechaFin

        fechas_validas_dict = validar_fechas(fecha_inicio_validar, fecha_fin_validar)

        if not fechas_validas_dict['valido']:
            logging.exception("Las fechas inicio y fin del evento son invalidas")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Las fechas inicio y fin del evento son invalidas'
            )

        params = {
            'nombre': request.nombre,
            'descripcion': request.descripcion,
            'fecha_inicio': request.fechaInicio,
            'fecha_fin': request.fechaFin,
            'categoria_evento_id': categoria_evento_id,
            'usuario_actualizacion_id': usuario_id,
            'estado': request.estado
        }

        if not params:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se encontró ningún campo para actualizar'
            )

        params['conexion'] = conexion

        params['evento_id'] = evento_id

        evento_actualizado = actualizar_evento_pg(**params)

        if not evento_actualizado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se pudo actualizar la categoria del evento'
            )

        conexion.commit()

        return

    except HTTPException as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e.detail)


    except Exception as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


    finally:
        conexion.close()
