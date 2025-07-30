import logging
from io import BytesIO
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File, Form, Query, Path
from starlette.responses import StreamingResponse

from database.connection import get_connection
from database.libro import registrar_libro_pg, obtener_libros_pg, obtener_content_libro
from models.generico import ResponseData, ResponseList
from models.libro import Libro
from shared.constante import Estado, Rol, SizeLibro
from shared.permission import get_current_user

router = APIRouter(prefix="/libro", tags=["Libro"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarLibro', status_code=status.HTTP_201_CREATED)
async def registrar_libro(
        editorialId: int = Form(...),
        titulo: str = Form(...),
        file: UploadFile = File(...),
        cantidadDisponible: int = Form(..., ge=1),
        sipnosis: str = Form(None),
        yearPublicacion: int = Form(None),
        archivoUrl: str = Form(None),
        imagenUrl: str = Form(None),
        current_user: dict = Depends(get_current_user(Rol.ADMINISTRADOR))):
    conexion = get_connection()

    try:

        content = await file.read()

        usuario_id = current_user['usuarioId']

        if len(content) > SizeLibro.MAX_FILE_SIZE:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                detail="Archivo excede los 20MB permitidos")

        libro_id = registrar_libro_pg(
            editorial_id=editorialId,
            titulo=titulo,
            estado=Estado.ACTIVO,
            content=content,
            usuario_creacion_id=usuario_id,
            cantidad_disponible=cantidadDisponible,
            sipnosis=sipnosis,
            year_publicacion=yearPublicacion,
            archivo_url=archivoUrl,
            imagen_url=imagenUrl,
            conexion=conexion
        )

        conexion.commit()

        return ResponseData[int](data=libro_id)

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


@router.get(
    "/",
    responses={status.HTTP_200_OK: {"model": ResponseList[List[Libro]]}},
    summary="obtenerLibros",
    status_code=status.HTTP_200_OK
)
def buscar_libros(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        estado: str | None = Query(None, min_length=2, max_length=2)
):
    conexion = get_connection()

    try:
        libros = obtener_libros_pg(
            estado=estado,
            conexion=conexion
        )

        if not libros:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron libros"
            )

        conexion.commit()
        return ResponseList(data=libros)

    except HTTPException as e:
        logging.exception("Error controlado al obtener libros")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado al obtener libros")
        conexion.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


    finally:
        conexion.close()


@router.get("/{libroId}/descargar",
            summary="Descargar contenido del libro por ID",
            status_code=status.HTTP_200_OK)
def descargar_libro(
        libroId: int = Path(..., description="ID del libro"),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
) -> StreamingResponse:
    conexion = get_connection()

    try:
        libros = obtener_libros_pg(libro_id=libroId, conexion=conexion)

        if not libros:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Libro no encontrado"
            )

        libro = libros[0]
        titulo = libro.titulo
        content = obtener_content_libro(libro_id=libroId)

        if content is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contenido del libro no disponible"
            )

        file_like = BytesIO(content)
        filename = f"{titulo.replace(' ', '_')}.pdf"

        return StreamingResponse(
            file_like,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException as e:
        logging.exception("Error esperado al descargar libro")
        raise e

    except Exception as e:
        logging.exception("Error inesperado al descargar libro")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

    finally:
        conexion.close()
