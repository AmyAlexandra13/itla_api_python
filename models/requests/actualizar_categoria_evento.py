
from pydantic import BaseModel, Field, field_validator

class ActualizarCategoriaEventoRequest(BaseModel):
    categoriaEventoId: int = Field(
        ge=1
    )

    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=250
    )

    estado: str = Field(
        min_length=2,
        max_length=2,
        pattern="^(IN|AC)$"
    )