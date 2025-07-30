from datetime import datetime
from pydantic import BaseModel

class Editorial(BaseModel):
    editorialId: int
    nombre: str
    estado: str
    fechaCreacion: datetime
    fechaActualizacion: datetime | None = None
