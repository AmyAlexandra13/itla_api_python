from pydantic import BaseModel, EmailStr
from typing import Optional


class RegistrarEditorialRequest(BaseModel):
    nombre: str
    estado: str