import logging

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path, Query

from database.connection import get_connection
from database.cuatrimestre import (
    registrar_cuatrimestre_pg,
    obtener_cuatrimestre_pg,
    actualizar_cuatrimestre_pg
)
from models.cuatrimestre import Cuatrimestre
from models.generico import ResponseData, ResponseList
from models.paginacion import ResponsePaginado
from models.requests.actualizar_cuatrimestre import ActualizarCuatrimestreRequest
from models.requests.registrar_cuatrimestre import RegistrarCuatrimestreRequest
from shared.constante import Estado, Rol
from shared.permission import get_current_user

router = APIRouter(prefix="/cuatrimestre", tags=["Cuatrimestre"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarCuatrimestre', status_code=status.HTTP_201_CREATED)
def registrar_cuatrimestre(
        request: RegistrarCuatrimestreRequest = Body(),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        cuatrimestres_existentes = obtener_cuatrimestre_pg(
            periodo=request.periodo,
            anio=request.anio,
            conexion=conexion
        )

        if cuatrimestres_existentes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un cuatrimestre para el periodo {request.periodo} del año {request.anio}"
            )

        cuatrimestre_id = registrar_cuatrimestre_pg(
            periodo=request.periodo,
            anio=request.anio,
            estado=Estado.ACTIVO,
            conexion=conexion
        )

        if not cuatrimestre_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo registrar el cuatrimestre"
            )

        conexion.commit()

        return ResponseData[int](data=cuatrimestre_id)

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
            responses={
                status.HTTP_200_OK: {
                    "model": ResponsePaginado[Cuatrimestre]
                }
            },
            summary='obtenerCuatrimestres', status_code=status.HTTP_200_OK)
def obtener_cuatrimestres(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        periodo: str | None = Query(
            None,
            description="Periodo del cuatrimestre",
            regex="^(C1|C2|C3)$"
        ),
        anio: int | None = Query(
            None,
            description="Año del cuatrimestre",
            ge=2000,
            le=2099
        ),
        estado: str | None = Query(
            None,
            description="Estado del cuatrimestre",
            regex="^(AC|IN)$"
        )
):
    conexion = get_connection()

    try:
        resultado = obtener_cuatrimestre_pg(
            periodo=periodo,
            anio=anio,
            estado=estado,
            conexion=conexion
        )

        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron cuatrimestres'
            )

        conexion.commit()

        return ResponseList(data=resultado)

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


@router.get("/{cuatrimestreId}",
            responses={status.HTTP_200_OK: {"model": ResponseData[Cuatrimestre]}},
            summary='obtenerCuatrimestrePorId', status_code=status.HTTP_200_OK)
def obtener_cuatrimestre_por_id(
        cuatrimestre_id: int = Path(alias='cuatrimestreId', description='ID del cuatrimestre'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        cuatrimestres = obtener_cuatrimestre_pg(
            cuatrimestre_id=cuatrimestre_id,
            conexion=conexion
        )

        if not cuatrimestres:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el cuatrimestre'
            )

        cuatrimestre = cuatrimestres[0]

        conexion.commit()

        return ResponseData(data=cuatrimestre)

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
              summary='actualizarCuatrimestre', status_code=status.HTTP_204_NO_CONTENT)
def actualizar_cuatrimestre(
        request: ActualizarCuatrimestreRequest = Body(),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        cuatrimestre_id = request.cuatrimestreId

        # Verificar que el cuatrimestre existe
        cuatrimestres = obtener_cuatrimestre_pg(
            cuatrimestre_id=cuatrimestre_id,
            conexion=conexion
        )

        if not cuatrimestres:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el cuatrimestre para actualizar'
            )

        if (request.periodo is None and request.anio is None and request.estado is None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se encontró ningún campo para actualizar'
            )

        # Si se actualiza periodo o año, verificar que no exista duplicado
        if request.periodo is not None or request.anio is not None:
            cuatrimestre_actual = cuatrimestres[0]
            periodo_verificar = request.periodo if request.periodo is not None else cuatrimestre_actual.periodo
            anio_verificar = request.anio if request.anio is not None else cuatrimestre_actual.anio

            cuatrimestres_duplicados = obtener_cuatrimestre_pg(
                periodo=periodo_verificar,
                anio=anio_verificar,
                conexion=conexion
            )

            if cuatrimestres_duplicados and cuatrimestres_duplicados[0].cuatrimestreId != cuatrimestre_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro cuatrimestre para el periodo {periodo_verificar} del año {anio_verificar}"
                )

        cuatrimestre_actualizado = actualizar_cuatrimestre_pg(
            cuatrimestre_id=cuatrimestre_id,
            periodo=request.periodo,
            anio=request.anio,
            estado=request.estado,
            conexion=conexion
        )

        if not cuatrimestre_actualizado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se pudo actualizar el cuatrimestre'
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
