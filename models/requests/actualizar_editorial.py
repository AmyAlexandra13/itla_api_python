from pydantic import BaseModel, EmailStr
from typing import Optional

class ActualizarEditorialRequest(BaseModel):
    nombre: str
    estado: str