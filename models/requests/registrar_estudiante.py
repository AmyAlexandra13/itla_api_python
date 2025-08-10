from pydantic import BaseModel, Field, EmailStr


class RegistrarEstudianteRequest(BaseModel):
    nombres: str = Field(min_length=1, max_length=250)
    apellidos: str = Field(min_length=1, max_length=250)
    correo: EmailStr = Field(min_length=1, max_length=50)
    cedula: str = Field(min_length=1, max_length=15)
    telefono: str = Field(min_length=1, max_length=15)
