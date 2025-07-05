import logging
from typing import List

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path

from database.categoria_evento import registrar_cateogoria_evento_pg, obtener_categoria_evento_pg, \
    actualizar_categoria_evento_pg
from database.connection import get_connection
from database.evento import registrar_evento_pg
from models.categoria_evento import CategoriaEvento
from models.generico import ResponseData, ResponseList
from models.requests.actualizar_categoria_evento import ActualizarCategoriaEventoRequest
from models.requests.registrar_categoria_evento import RegistrarCategoriaEventoRequest
from models.requests.registrar_evento import RegistrarEventoRequest
from shared.constante import Estado, Rol
from shared.permission import get_current_user
from shared.utils import validar_fechas

router = APIRouter(prefix="/evento", tags=["Evento"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarEvento', status_code=status.HTTP_201_CREATED)
def registrar_categoria_evento(request: RegistrarEventoRequest = Body(),
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
            responses={status.HTTP_200_OK: {"model": ResponseList[List[CategoriaEvento]]}},
            summary='obtenerCategoriaEvento', status_code=status.HTTP_200_OK)
def buscar_categoria_evento(_: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):
    conexion = get_connection()

    try:

        categorias_eventos = obtener_categoria_evento_pg(
            conexion=conexion
        )

        if not categorias_eventos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron categorias de eventos'
            )

        conexion.commit()

        return ResponseList(data=categorias_eventos)

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

@router.get("/{categoriaEventoId}",
             responses={status.HTTP_200_OK: {"model": ResponseData[CategoriaEvento]}},
             summary='registrarCategoriaEvento', status_code=status.HTTP_200_OK)
def buscar_categoria_evento_id(categoria_evento_id: int = Path(alias='categoriaEventoId', description='Id de la categoria del evento'),
              _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):

    conexion = get_connection()

    try:

        categorias_eventos = obtener_categoria_evento_pg(
            categoria_evento_id=categoria_evento_id,
            conexion=conexion
        )

        if not categorias_eventos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró la categoria del evento'
            )

        categoria_evento = categorias_eventos[0]


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
             summary='actualizarCategoriaEvento', status_code=status.HTTP_204_NO_CONTENT)
def actualizar_categoria_evento(request: ActualizarCategoriaEventoRequest = Body(),
              _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):

    conexion = get_connection()

    try:

        categoria_evento_id = request.categoriaEventoId

        categorias_eventos = obtener_categoria_evento_pg(
            categoria_evento_id=categoria_evento_id,
            conexion=conexion
        )

        if not categorias_eventos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró la categoria del evento para actualizar'
            )


        params = {
            'nombre': request.nombre,
            'estado': request.estado
        }

        if not params:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se encontró ningún campo para actualizar'
            )

        params['conexion'] = conexion

        params['categoria_evento_id'] = categoria_evento_id

        categoria_evento_actualizado = actualizar_categoria_evento_pg(**params)

        if not categoria_evento_actualizado:
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

