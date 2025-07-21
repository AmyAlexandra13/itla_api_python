import logging

from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File, Form

from database.connection import get_connection
from database.libro import registrar_libro_pg
from models.generico import ResponseData
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
