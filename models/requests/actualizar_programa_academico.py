import re

from pydantic import BaseModel, Field, field_validator


class ActualizarProgramaAcademicoRequest(BaseModel):
    programaAcademicoId: int = Field(ge=1)
    nombre: str | None = Field(default=None, min_length=1, max_length=250)
    estado: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
        pattern="^(AC|IN)$"
    )
    periodoAcademico: str | None = Field(
        default=None,
        pattern=r"^\d{4}-\d{4}$",
        description="Formato: 2025-2026 con años consecutivos"
    )

    @field_validator("periodoAcademico")
    def validar_periodo_consecutivo(cls, v):
        if v is None:
            return v
        match = re.match(r"^(\d{4})-(\d{4})$", v)
        if match:
            inicio, fin = map(int, match.groups())
            if fin - inicio < 1:
                raise ValueError("Los años del periodo académico deben ser consecutivos (ej: 2025-2026)")
        return v
