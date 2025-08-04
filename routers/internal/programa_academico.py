import logging
from typing import List

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path, Query

from database.connection import get_connection
from database.programa_academico import (
    registrar_programa_academico_pg,
    obtener_programa_academico_pg,
    actualizar_programa_academico_pg
)
from models.generico import ResponseData, ResponseList
from models.programa_academico import ProgramaAcademico
from models.requests.actualizar_programa_academico import ActualizarProgramaAcademicoRequest
from models.requests.registrar_programa_academico import RegistrarProgramaAcademicoRequest
from shared.constante import Estado, Rol
from shared.permission import get_current_user

router = APIRouter(prefix="/programa-academico", tags=["Programa Académico"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarProgramaAcademico', status_code=status.HTTP_201_CREATED)
def registrar_programa_academico(
        request: RegistrarProgramaAcademicoRequest = Body(),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        programa_academico_id = registrar_programa_academico_pg(
            nombre=request.nombre,
            periodo_academico=request.periodoAcademico,
            estado=Estado.ACTIVO,
            conexion=conexion
        )

        if not programa_academico_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo registrar el programa académico"
            )

        conexion.commit()

        return ResponseData[int](data=programa_academico_id)

    except HTTPException as e:
        logging.exception("Error controlado")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.get("/",
            responses={status.HTTP_200_OK: {"model": ResponseList[List[ProgramaAcademico]]}},
            summary='obtenerProgramasAcademicos', status_code=status.HTTP_200_OK)
def obtener_programas_academicos(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        estado: str | None = Query(None, min_length=2, max_length=2, pattern="^(AC|IN)$")
):
    conexion = get_connection()

    try:
        programas_academicos = obtener_programa_academico_pg(
            estado=estado,
            conexion=conexion
        )

        if not programas_academicos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron programas académicos'
            )

        conexion.commit()

        return ResponseList(data=programas_academicos)

    except HTTPException as e:
        logging.exception("Error controlado")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.get("/{programaAcademicoId}",
            responses={status.HTTP_200_OK: {"model": ResponseData[ProgramaAcademico]}},
            summary='obtenerProgramaAcademicoPorId', status_code=status.HTTP_200_OK)
def obtener_programa_academico_por_id(
        programa_academico_id: int = Path(alias='programaAcademicoId', description='ID del programa académico'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        programas_academicos = obtener_programa_academico_pg(
            programa_academico_id=programa_academico_id,
            conexion=conexion
        )

        if not programas_academicos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el programa académico'
            )

        programa_academico = programas_academicos[0]

        conexion.commit()

        return ResponseData(data=programa_academico)

    except HTTPException as e:
        logging.exception("Error controlado")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.patch("/actualizar",
              summary='actualizarProgramaAcademico', status_code=status.HTTP_204_NO_CONTENT)
def actualizar_programa_academico(
        request: ActualizarProgramaAcademicoRequest = Body(),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        programa_academico_id = request.programaAcademicoId

        # Verificar que el programa académico existe
        programas_academicos = obtener_programa_academico_pg(
            programa_academico_id=programa_academico_id,
            conexion=conexion
        )

        if not programas_academicos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el programa académico para actualizar'
            )

        # Validar que al menos un campo se va a actualizar
        if request.nombre is None and request.estado is None and request.periodoAcademico is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se encontró ningún campo para actualizar'
            )

        programa_academico_actualizado = actualizar_programa_academico_pg(
            programa_academico_id=programa_academico_id,
            nombre=request.nombre,
            estado=request.estado,
            periodo_academico=request.periodoAcademico,
            conexion=conexion
        )

        if not programa_academico_actualizado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se pudo actualizar el programa académico'
            )

        conexion.commit()

        return

    except HTTPException as e:
        logging.exception("Error controlado")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()
