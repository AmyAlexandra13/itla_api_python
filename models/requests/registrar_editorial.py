from pydantic import BaseModel, Field

class RegistrarEditorialRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=250)
