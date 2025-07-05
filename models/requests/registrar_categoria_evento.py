
from pydantic import BaseModel, Field, field_validator

class RegistrarCategoriaEventoRequest(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=250
    )