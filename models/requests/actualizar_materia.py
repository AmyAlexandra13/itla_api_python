from typing import List

from pydantic import BaseModel, Field


class ActualizarMateriaRequest(BaseModel):
    materiaId: int = Field(ge=1)
    nombre: str | None = Field(default=None, min_length=1, max_length=250)
    codigo: str | None = Field(default=None, min_length=1, max_length=20)
    estado: str | None = Field(default=None, min_length=2, max_length=2, pattern="^(AC|IN)$")
    credito: int | None = Field(default=None, ge=1)
    programasAcademicosIds: List[int] | None = Field(default=None,
                                                     description="IDs de programas académicos a los que pertenece la materia")
