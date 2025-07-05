from pydantic import BaseModel, Field


class ActualizarCategoriaEventoRequest(BaseModel):
    categoriaEventoId: int = Field(
        ge=1
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


