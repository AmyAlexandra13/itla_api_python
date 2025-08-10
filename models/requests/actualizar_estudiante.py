from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ActualizarEstudianteRequest(BaseModel):
    estudianteId: int = Field(
        gt=0,
        description="Identificador único del estudiante"
    )

    nombres: Optional[str] = Field(
        None,
        description="Nombres del estudiante",
        min_length=2,
        max_length=100
    )

    apellidos: Optional[str] = Field(
        None,
        description="Apellidos del estudiante",
        min_length=2,
        max_length=100
    )

    correo: Optional[EmailStr] = Field(
        None,
        description="Correo electrónico del estudiante"
    )

    estado: Optional[str] = Field(
        None,
        description="Estado del estudiante",
        pattern="^(REGISTRADO|PENDIENTE_DOCUMENTO|PENDIENTE_RESPUESTA|ACEPTADO|RECHAZADO|GRADUADO)$"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "estudianteId": 1,
                "nombres": "Juan Carlos",
                "apellidos": "Pérez González",
                "correo": "juan.perez@correo.com",
                "estado": "ACEPTADO"
            }
        }