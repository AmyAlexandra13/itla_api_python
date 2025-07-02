from pydantic import BaseModel, Field, EmailStr


class LoginUsuario(BaseModel):
    correo: EmailStr = Field(
        min_length=1,
        max_length=250
    )

    clave: str = Field(
        min_length=1,
        max_length=250
    )
