from datetime import datetime

from pydantic import BaseModel


class ProgramaAcademico(BaseModel):
    programaAcademicoId: int
    nombre: str
    estado: str
    periodoAcademico: str
    fechaCreacion: datetime
    fechaActualizacion: datetime | None = None
