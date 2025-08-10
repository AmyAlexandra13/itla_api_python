from decimal import Decimal
from pydantic import BaseModel, Field


class ActualizarEstudianteMateriaRequest(BaseModel):
    estudianteMateriaId: int = Field(ge=1, description="ID del registro estudiante-materia")

    estado: str | None = Field(
        default=None,
        pattern="^(RETIRADA|APROBADA|REPROBADA)$",
        description="Estado de la materia del estudiante"
    )

    calificacion: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        decimal_places=2,
        description="Calificación del estudiante en la materia"
    )