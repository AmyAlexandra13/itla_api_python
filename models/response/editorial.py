from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EditorialResponse(BaseModel):
    id: int
    nombre: str
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[bool] = True
    fecha_creacion: datetime

    model_config = {
        "from_attributes": True
    }
