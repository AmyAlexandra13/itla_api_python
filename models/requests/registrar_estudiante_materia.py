from decimal import Decimal
from pydantic import BaseModel, Field


class RegistrarEstudianteMateriaRequest(BaseModel):
    estudianteId: int = Field(ge=1, description="ID del estudiante")
    materiaId: int = Field(ge=1, description="ID de la materia")
    cuatrimestreId: int = Field(ge=1, description="ID del cuatrimestre")
    estado: str = Field(
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