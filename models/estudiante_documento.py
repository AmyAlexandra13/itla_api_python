from typing import Optional, Dict, Any
from pydantic import BaseModel


class EstudianteDocumento(BaseModel):
    estudianteDocumentoId: int
    estudianteId: int
    tipoDocumento: str
    estado: str
    fechaCreacion: str
    fechaActualizacion: Optional[str] = None
    estudiante: Dict[str, Any]

    class Config:
        from_attributes = True