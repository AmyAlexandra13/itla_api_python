import logging
from typing import List

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path, Query

from database.materia import (
    registrar_materia_pg,
    obtener_materia_pg,
    actualizar_materia_pg,
    registrar_programa_academico_materia_pg,
    eliminar_programa_academico_materia_pg,
    obtener_programa_academico_materia_por_materia_pg
)
from database.programa_academico import obtener_programa_academico_pg
from database.connection import get_connection
from models.materia import Materia
from models.generico import ResponseData, ResponseList
from models.requests.registrar_materia import RegistrarMateriaRequest
from models.requests.actualizar_materia import ActualizarMateriaRequest
from shared.constante import Estado, Rol
from shared.permission import get_current_user

router = APIRouter(prefix="/materia", tags=["Materia"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarMateria', status_code=status.HTTP_201_CREATED)
def registrar_materia(
        request: RegistrarMateriaRequest = Body(),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        # Verificar que el código no esté duplicado
        materias_existentes = obtener_materia_pg(
            codigo=request.codigo,
            conexion=conexion
        )

        if materias_existentes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una materia con ese código"
            )


        for programa_id in request.programasAcademicosIds:
            programas = obtener_programa_academico_pg(
                programa_academico_id=programa_id,
                estado=Estado.ACTIVO,
                conexion=conexion
            )
            if not programas:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se encontró el programa académico con ID {programa_id} o está inactivo"
                )

        # Registrar la materia
        materia_id = registrar_materia_pg(
            nombre=request.nombre,
            codigo=request.codigo,
            credito=request.credito,
            estado=Estado.ACTIVO,
            conexion=conexion
        )

        if not materia_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo registrar la materia"
            )

        # Registrar las relaciones con programas académicos
        if request.programasAcademicosIds:
            for programa_id in request.programasAcademicosIds:
                registrar_programa_academico_materia_pg(
                    programa_academico_id=programa_id,
                    materia_id=materia_id,
                    estado=Estado.ACTIVO,
                    conexion=conexion
                )

        conexion.commit()

        return ResponseData[int](data=materia_id)

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
            responses={status.HTTP_200_OK: {"model": ResponseList[List[Materia]]}},
            summary='obtenerMaterias', status_code=status.HTTP_200_OK)
def obtener_materias(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        estado: str | None = Query(None, min_length=2, max_length=2, pattern="^(AC|IN)$")
):
    conexion = get_connection()

    try:
        materias = obtener_materia_pg(
            estado=estado,
            conexion=conexion
        )

        if not materias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron materias'
            )

        conexion.commit()

        return ResponseList(data=materias)

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


@router.get("/{materiaId}",
            responses={status.HTTP_200_OK: {"model": ResponseData[Materia]}},
            summary='obtenerMateriaPorId', status_code=status.HTTP_200_OK)
def obtener_materia_por_id(
        materia_id: int = Path(alias='materiaId', description='ID de la materia'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        materias = obtener_materia_pg(
            materia_id=materia_id,
            conexion=conexion
        )

        if not materias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró la materia'
            )

        materia = materias[0]

        conexion.commit()

        return ResponseData(data=materia)

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
              summary='actualizarMateria', status_code=status.HTTP_204_NO_CONTENT)
def actualizar_materia(
        request: ActualizarMateriaRequest = Body(),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        materia_id = request.materiaId

        # Verificar que la materia existe
        materias = obtener_materia_pg(
            materia_id=materia_id,
            conexion=conexion
        )

        if not materias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró la materia para actualizar'
            )

        # Validar que al menos un campo se va a actualizar
        if (request.nombre is None and request.codigo is None and
            request.estado is None and request.credito is None and
            request.programasAcademicosIds is None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se encontró ningún campo para actualizar'
            )

        # Verificar que el código no esté duplicado (si se está actualizando)
        if request.codigo is not None:
            materias_con_codigo = obtener_materia_pg(
                codigo=request.codigo,
                conexion=conexion
            )
            if materias_con_codigo and materias_con_codigo[0].materiaId != materia_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otra materia con ese código"
                )

        # Validar que los programas académicos existen (si se están actualizando)
        if request.programasAcademicosIds is not None:
            for programa_id in request.programasAcademicosIds:
                programas = obtener_programa_academico_pg(
                    programa_academico_id=programa_id,
                    estado=Estado.ACTIVO,
                    conexion=conexion
                )
                if not programas:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"No se encontró el programa académico con ID {programa_id} o está inactivo"
                    )

        # Actualizar la materia
        materia_actualizada = actualizar_materia_pg(
            materia_id=materia_id,
            nombre=request.nombre,
            codigo=request.codigo,
            estado=request.estado,
            credito=request.credito,
            conexion=conexion
        )

        if not materia_actualizada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se pudo actualizar la materia'
            )

        # Actualizar relaciones con programas académicos si se especificaron
        if request.programasAcademicosIds is not None:
            # Eliminar relaciones existentes
            eliminar_programa_academico_materia_pg(
                materia_id=materia_id,
                conexion=conexion
            )

            # Crear nuevas relaciones
            for programa_id in request.programasAcademicosIds:
                registrar_programa_academico_materia_pg(
                    programa_academico_id=programa_id,
                    materia_id=materia_id,
                    estado=Estado.ACTIVO,
                    conexion=conexion
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


@router.get("/{materiaId}/programas-academicos",
            responses={status.HTTP_200_OK: {"model": ResponseList[List[int]]}},
            summary='obtenerProgramasAcademicosDeMateria', status_code=status.HTTP_200_OK)
def obtener_programas_academicos_de_materia(
        materia_id: int = Path(alias='materiaId', description='ID de la materia'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        # Verificar que la materia existe
        materias = obtener_materia_pg(
            materia_id=materia_id,
            conexion=conexion
        )

        if not materias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró la materia'
            )

        programas_ids = obtener_programa_academico_materia_por_materia_pg(
            materia_id=materia_id,
            conexion=conexion
        )

        conexion.commit()

        return ResponseList(data=programas_ids)

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