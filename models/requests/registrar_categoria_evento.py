#haz un modelo registrar categoria evento request de la estructura categoria evento

from pydantic import BaseModel, Field, field_validator

class RegistrarCategoriaEventoRequest(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=250
    )