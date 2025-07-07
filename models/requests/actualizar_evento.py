# models/requests/actualizar_evento.py
from pydantic import BaseModel, Field
from datetime import datetime

class ActualizarEventoRequest(BaseModel):
    eventoId: int = Field(
        ge=1, alias="eventoId"
    )
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=250
    )
    estado: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
        pattern="^(IN|AC)$"
    )
    descripcion: str | None = Field(
        default=None,
        min_length=1,
        max_length=250
    )
    categoriaEventoId: int | None = Field(
        default=None,
        ge=1, alias="categoriaEventoId"
    )
    fechaInicio: datetime | None = Field(
        default=None, alias="fechaInicio"
    )
    fechaFin: datetime | None = Field(
        default=None, alias="fechaFin"
    )