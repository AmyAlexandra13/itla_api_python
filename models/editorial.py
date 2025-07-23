from pydantic import BaseModel
from datetime import datetime

class RegistrarEditorialRequest(BaseModel):
    nombre: str
    estado: str

class ActualizarEditorialRequest(BaseModel):
    nombre: str
    estado: str

class EditorialResponse(BaseModel):
    editorial_id: int
    nombre: str
    estado: str
    fecha_creacion: datetime
