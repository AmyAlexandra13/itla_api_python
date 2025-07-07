# models/evento.py
from pydantic import BaseModel, Field
from datetime import datetime

class CategoriaEventoSimple(BaseModel):
    categoria_evento_id: int = Field(alias='categoriaEventoId')
    nombre: str

class Evento(BaseModel):
    evento_id: int = Field(alias='eventoId')
    nombre: str
    descripcion: str | None = None
    fecha_inicio: datetime = Field(alias='fechaInicio')
    fecha_fin: datetime = Field(alias='fechaFin')
    estado: str
    categoria_evento: CategoriaEventoSimple = Field(alias='categoriaEvento')

    @classmethod
    def from_dict(cls, data: dict):
        # Este método convierte un diccionario de la base de datos a un objeto Evento
        return cls(
            eventoId=data.get('evento_id'),
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            fechaInicio=data.get('fecha_inicio'),
            fechaFin=data.get('fecha_fin'),
            estado=data.get('estado'),
            categoriaEvento={
                'categoriaEventoId': data.get('categoria_evento_id'),
                'nombre': data.get('categoria_nombre')
            }
        )