from pydantic import BaseModel, Field


class RegistrarCuatrimestreRequest(BaseModel):
    periodo: str = Field(
        min_length=2,
        max_length=2,
        pattern="^(C1|C2|C3)$",
        description="Periodo del cuatrimestre: C1, C2 o C3"
    )
    anio: int = Field(
        ge=2000,
        le=2099,
        description="Año del cuatrimestre"
    )