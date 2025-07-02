from pydantic import BaseModel, Field, EmailStr


class RegistrarUsuarioModel(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=250
    )

    correo: EmailStr = Field(
        min_length=1,
        max_length=250
    )

    clave: str = Field(
        min_length=1,
        max_length=250
    )

    rolId: int = Field(
        gt=0,
        le=3
    )
