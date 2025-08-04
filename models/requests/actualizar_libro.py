from typing import Optional
from pydantic import BaseModel, Field


class ActualizarLibroRequest(BaseModel):
    libroId: int = Field(ge=1)
    editorialId: Optional[int] = Field(default=None, ge=1)
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=250)
    estado: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=2,
        pattern="^(AC|IN)$"
    )
    cantidadDisponible: Optional[int] = Field(default=None, ge=1)
    sipnosis: Optional[str] = Field(default=None, min_length=1, max_length=250)
    yearPublicacion: Optional[int] = Field(default=None, ge=1000, le=9999)
    archivoUrl: Optional[str] = Field(default=None, min_length=1, max_length=250)
    imagenUrl: Optional[str] = Field(default=None, min_length=1, max_length=250)