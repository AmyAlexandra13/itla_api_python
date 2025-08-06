from typing import List

from pydantic import BaseModel, Field


class RegistrarMateriaRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=250)
    codigo: str = Field(min_length=1, max_length=20)
    credito: int = Field(ge=1)
    programasAcademicosIds: List[int] = Field(
        description="IDs de programas académicos a los que pertenece la materia")
