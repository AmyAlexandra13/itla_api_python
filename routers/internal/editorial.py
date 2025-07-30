import logging
from typing import List

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path, Query

from database.editorial import registrar_editorial_pg, obtener_editorial_pg, actualizar_editorial_pg
from database.connection import get_connection
from models.editorial import Editorial
from models.generico import ResponseData, ResponseList
from models.requests.registrar_editorial import RegistrarEditorialRequest
from models.requests.actualizar_editorial import ActualizarEditorialRequest
from shared.constante import Estado, Rol
from shared.permission import get_current_user

router = APIRouter(prefix="/editorial", tags=["Editorial"])

@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarEditorial', status_code=status.HTTP_201_CREATED)
def registrar_editorial(request: RegistrarEditorialRequest = Body(),
                        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):
    conexion = get_connection()

    try:
        editorial_id = registrar_editorial_pg(
            nombre=request.nombre,
            estado=Estado.ACTIVO,
            conexion=conexion
        )

        conexion.commit()

        return ResponseData[int](data=editorial_id)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.get("/",
            responses={status.HTTP_200_OK: {"model": ResponseList[List[Editorial]]}},
            summary='obtenerEditorial', status_code=status.HTTP_200_OK)
def obtener_editoriales(_: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
                         estado: str | None = Query(None, min_length=2, max_length=2, pattern="^(AC|IN)$")):
    conexion = get_connection()

    try:
        editoriales = obtener_editorial_pg(estado=estado, conexion=conexion)

        if not editoriales:
            raise HTTPException(status_code=404, detail="No se encontraron editoriales")

        conexion.commit()
        return ResponseList(data=editoriales)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conexion.close()


@router.get("/{editorialId}",
            responses={status.HTTP_200_OK: {"model": ResponseData[Editorial]}},
            summary='obtenerEditorialPorId', status_code=status.HTTP_200_OK)
def obtener_editorial_id(editorial_id: int = Path(alias="editorialId", ge=1),
                         _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
                         estado: str | None = Query(None, pattern="^(AC|IN)$")):
    conexion = get_connection()

    try:
        editoriales = obtener_editorial_pg(
            editorial_id=editorial_id,
            estado=estado,
            conexion=conexion
        )

        if not editoriales:
            raise HTTPException(status_code=404, detail="No se encontró la editorial")

        conexion.commit()
        return ResponseData(data=editoriales[0])

    except HTTPException as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e.detail)


    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conexion.close()


@router.patch("/actualizar",
              summary="actualizarEditorial", status_code=status.HTTP_204_NO_CONTENT)
def actualizar_editorial(request: ActualizarEditorialRequest = Body(),
                         _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):
    conexion = get_connection()

    try:
        if request.nombre is None and request.estado is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe enviar al menos un dato para actualizar la editorial"
            )

        editoriales = obtener_editorial_pg(editorial_id=request.editorialId, conexion=conexion)

        if not editoriales:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró la editorial para actualizar")

        actualizado = actualizar_editorial_pg(
            editorial_id=request.editorialId,
            nombre=request.nombre,
            estado=request.estado,
            conexion=conexion
        )

        if not actualizado:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la editorial")

        conexion.commit()
        return

    except HTTPException as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conexion.close()
