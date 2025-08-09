from pydantic import BaseModel, Field


class ActualizarDocumentoRequest(BaseModel):
    documentoId: int = Field(
        ge=1,
        description="ID del documento a actualizar"
    )

    estudianteId: int = Field(
        ge=1,
        description="ID del estudiante propietario del documento"
    )

    estado: str = Field(
        max_length=10,
        pattern="^(PENDIENTE|VALIDO|RECHAZADO)$",
        description="Nuevo estado del documento"
    )
