import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException, Query

from models.generico import ResponseData, ResponseList
from models.unicda.evento_unicda import EventosUNICDAPaginadoResponse
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
            responses={status.HTTP_200_OK: {"model": ResponseData[EventosUNICDAPaginadoResponse]}},
            summary='obtenerEventosUNICDA', status_code=status.HTTP_200_OK)
def obtener_eventos_unicda(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        fechaInicio: Optional[datetime] = Query(None, description="Fecha de inicio para filtrar eventos"),
        fechaFin: Optional[datetime] = Query(None, description="Fecha de fin para filtrar eventos")
):
    """
    Obtiene la lista de eventos paginada desde la API de UNICDA
    """
    try:
        params = {
            "page": UnicdaPaginacion.PAGE,
            "pageSize": UnicdaPaginacion.PAGESIZE
        }


        if fechaInicio is not None:
            params["FromDate"] = fechaInicio.isoformat()

        if fechaFin is not None:
            params["ToDate"] = fechaFin.isoformat()

        # Validar que si se proporciona fechaInicio, también se proporcione fechaFin
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

        # Validar que fechaInicio sea menor que fechaFin
        if fechaInicio is not None and fechaFin is not None:
            if fechaInicio >= fechaFin:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La fechaInicio debe ser menor que la fechaFin"
                )

        # Realizar petición a UNICDA
        response = unicda_service.get(UNICDAEndpoints.EVENTOS_PAGINATION, params=params)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al obtener eventos de UNICDA"
            )

        # Validar que la respuesta tenga la estructura esperada
        if "pagination" not in response or "data" not in response:
            logging.error(f"Respuesta inesperada de UNICDA: {response}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Formato de respuesta inesperado de UNICDA"
            )


        # Convertir la respuesta al modelo esperado
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