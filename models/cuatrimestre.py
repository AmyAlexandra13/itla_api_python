from datetime import datetime
from pydantic import BaseModel


class Cuatrimestre(BaseModel):
    cuatrimestreId: int
    periodo: str
    anio: int
    estado: str
    fechaCreacion: datetime
    fechaActualizacion: datetime | None = None