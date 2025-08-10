import logging
from datetime import datetime
from io import BytesIO
from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException, Query, Path
from starlette.responses import StreamingResponse

from models.generico import ResponseData, ResponseList
from models.unicda.evento_unicda import EventosUNICDAPaginadoResponse, EventoUNICDA
from models.unicda.libro_unicda import LibrosUNICDAPaginadoResponse, LibroUNICDA
from models.unicda_token_response import UNICDATokenResponse
from shared.constante import Rol, UNICDAEndpoints, UnicdaPaginacion
from shared.permission import get_current_user
from shared.unicda_service import unicda_service

router = APIRouter(prefix="/unicda", tags=["UNICDA"])


@router.post("/generar-token",
             responses={status.HTTP_200_OK: {"model": ResponseData[UNICDATokenResponse]}},
             summary='generarTokenUNICDA', status_code=status.HTTP_200_OK)
def generar_token_unicda(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    try:
        token = unicda_service.get_valid_token()

        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo generar el token de UNICDA"
            )

        expiry_str = unicda_service.token_expiry.isoformat() if unicda_service.token_expiry else "No disponible"

        response_data = UNICDATokenResponse(
            token=token,
            expiry=expiry_str,
            message="Token generado exitosamente"
        )

        return ResponseData(data=response_data)

    except Exception as e:
        logging.exception("Error inesperado al generar token de UNICDA")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/eventos",
            responses={status.HTTP_200_OK: {"model": ResponseList[EventoUNICDA]}},
            summary='obtenerEventosUNICDA', status_code=status.HTTP_200_OK)
def obtener_eventos_unicda(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        fechaInicio: Optional[datetime] = Query(None, description="Fecha de inicio para filtrar eventos"),
        fechaFin: Optional[datetime] = Query(None, description="Fecha de fin para filtrar eventos")
):
    try:
        params = {
            "page": UnicdaPaginacion.PAGE,
            "pageSize": UnicdaPaginacion.PAGESIZE
        }

        if fechaInicio is not None:
            params["FromDate"] = fechaInicio.isoformat()

        if fechaFin is not None:
            params["ToDate"] = fechaFin.isoformat()

        if fechaInicio is not None and fechaFin is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Si proporciona fechaInicio, también debe proporcionar fechaFin"
            )

        if fechaFin is not None and fechaInicio is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Si proporciona fechaFin, también debe proporcionar fechaInicio"
            )

        if fechaInicio is not None and fechaFin is not None:
            if fechaInicio >= fechaFin:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La fechaInicio debe ser menor que la fechaFin"
                )

        response = unicda_service.get(UNICDAEndpoints.EVENTOS_PAGINATION, params=params)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al obtener eventos de UNICDA"
            )

        if "pagination" not in response or "data" not in response:
            logging.error(f"Respuesta inesperada de UNICDA: {response}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Formato de respuesta inesperado de UNICDA"
            )

        try:
            eventos_response = EventosUNICDAPaginadoResponse(**response)

            data_evento = eventos_response.data

            return ResponseList(data=data_evento)
        except Exception as parse_error:
            logging.error(f"Error al parsear respuesta de eventos UNICDA: {str(parse_error)}")
            logging.error(f"Respuesta original: {response}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al procesar la respuesta de UNICDA"
            )

    except HTTPException as e:
        logging.exception("Error controlado")

        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.exception("Error inesperado al obtener eventos de UNICDA")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/libros",
            responses={status.HTTP_200_OK: {"model": ResponseList[LibroUNICDA]}},
            summary='obtenerLibrosUNICDA', status_code=status.HTTP_200_OK)
def obtener_libros_unicda(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        titulo: Optional[str] = Query(None, description="Título del libro para filtrar"),
        editorialId: Optional[int] = Query(None, ge=1, description="ID de la editorial para filtrar")
):
    """
    Obtiene la lista de libros desde la API de UNICDA
    """
    try:
        # Construir parámetros para la petición
        params = {
            "Page": UnicdaPaginacion.PAGE,
            "PageSize": UnicdaPaginacion.PAGESIZE
        }

        # Agregar parámetros opcionales si se proporcionan
        if titulo is not None:
            params["titulo"] = titulo

        if editorialId is not None:
            params["editorialId"] = editorialId

        # Realizar petición a UNICDA
        response = unicda_service.get(UNICDAEndpoints.LIBROS_PAGINATION, params=params)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al obtener libros de UNICDA"
            )

        # Validar que la respuesta tenga la estructura esperada
        if "pagination" not in response or "data" not in response:
            logging.error(f"Respuesta inesperada de UNICDA libros: {response}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Formato de respuesta inesperado de UNICDA"
            )

        try:
            libros_response = LibrosUNICDAPaginadoResponse(**response)

            data_libros = libros_response.data

            return ResponseList(data=data_libros)

        except Exception as parse_error:
            logging.error(f"Error al parsear respuesta de libros UNICDA: {str(parse_error)}")
            logging.error(f"Respuesta original: {response}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al procesar la respuesta de UNICDA"
            )

    except HTTPException as e:
        logging.exception("Error controlado")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.exception("Error inesperado al obtener libros de UNICDA")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/pdf/{fileUrl:path}",
            summary="Descargar PDF desde UNICDA",
            status_code=status.HTTP_200_OK)
def descargar_pdf_unicda(
        fileUrl: str = Path(..., description="URL del archivo PDF en UNICDA"),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
) -> StreamingResponse:
    try:
        endpoint = f"{UNICDAEndpoints.PDF_MULTIMEDIA}/{fileUrl}"

        pdf_content = unicda_service.get_pdf(endpoint)

        if pdf_content is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo obtener el archivo PDF de UNICDA"
            )

        if not pdf_content.startswith(b'%PDF'):
            logging.error("El contenido recibido no es un archivo PDF válido")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El archivo obtenido no es un PDF válido"
            )

        pdf_buffer = BytesIO(pdf_content)

        filename_base = fileUrl.replace('/', '_').replace('\\', '_').replace(':', '_')

        if not filename_base.lower().endswith('.pdf'):
            filename_base += '.pdf'

        filename = f"unicda_documento_{filename_base}"

        return StreamingResponse(
            BytesIO(pdf_content),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException as e:
        logging.exception("Error controlado al descargar PDF de UNICDA")
        raise e

    except Exception as e:
        logging.exception("Error inesperado al descargar PDF de UNICDA")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )
