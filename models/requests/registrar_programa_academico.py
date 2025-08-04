import re

from pydantic import BaseModel, Field, field_validator


class RegistrarProgramaAcademicoRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=250)
    periodoAcademico: str = Field(
        pattern=r"^\d{4}-\d{4}$",
        description="Formato: 2025-2026 con años consecutivos"
    )

    @field_validator("periodoAcademico")
    def validar_periodo_consecutivo(cls, v):
        match = re.match(r"^(\d{4})-(\d{4})$", v)
        if match:
            inicio, fin = map(int, match.groups())
            if fin - inicio < 0:
                raise ValueError("Los años del periodo académico deben ser consecutivos (ej: 2025-2026)")
        return v
