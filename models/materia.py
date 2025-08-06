from datetime import datetime
from pydantic import BaseModel

class Materia(BaseModel):
    materiaId: int
    nombre: str
    codigo: str
    estado: str
    credito: int
    fechaCreacion: datetime
    fechaActualizacion: datetime | None = None