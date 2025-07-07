# models/requests/registrar_evento.py
from pydantic import BaseModel, Field
from datetime import datetime

class RegistrarEventoRequest(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=250
    )
    descripcion: str | None = Field(
        default=None,
        min_length=1,
        max_length=250
    )
    categoriaEventoId: int = Field(
        gt=0, alias="categoriaEventoId"
    )
    fechaInicio: datetime = Field(alias="fechaInicio")
    fechaFin: datetime = Field(alias="fechaFin")
