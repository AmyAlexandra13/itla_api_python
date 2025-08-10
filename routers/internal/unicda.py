import logging

from fastapi import APIRouter, status, Depends, HTTPException

from models.generico import ResponseData
from models.unicda_token_response import UNICDATokenResponse
from shared.constante import Rol
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
