from pydantic import BaseModel, EmailStr
from typing import Optional

class RegistrarEditorialRequest(BaseModel):
    nombre: str
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[bool] = True