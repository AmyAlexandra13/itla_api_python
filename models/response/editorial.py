from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EditorialResponse(BaseModel):
    editorial_id: int
    nombre: str
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime | None = None