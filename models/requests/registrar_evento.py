from datetime import datetime

from pydantic import BaseModel, Field, field_validator

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
        gt=0
    )

    fechaInicio: datetime

    fechaFin: datetime

