from pydantic import BaseModel, Field


class ActualizarCuatrimestreRequest(BaseModel):
    cuatrimestreId: int = Field(ge=1)

    periodo: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
        pattern="^(C1|C2|C3)$",
        description="Periodo del cuatrimestre: C1, C2 o C3"
    )

    anio: int | None = Field(
        default=None,
        ge=2000,
        le=2099,
        description="Año del cuatrimestre"
    )

    estado: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
        pattern="^(AC|IN)$",
        description="Estado: AC (Activo) o IN (Inactivo)"
    )