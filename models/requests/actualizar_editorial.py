from pydantic import BaseModel, EmailStr
from typing import Optional

class ActualizarEditorialRequest(BaseModel):
    nombre: Optional[str]
    correo: Optional[EmailStr]
    telefono: Optional[str]
    direccion: Optional[str]
    estado: Optional[bool]

    model_config = {
        "from_attributes": True
    }
