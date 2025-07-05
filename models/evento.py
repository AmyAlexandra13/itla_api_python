from datetime import datetime

from pydantic import BaseModel

class UsuarioEvento(BaseModel):
    usuarioId: int
    nombre: str

class CategoriaEventoEvento(BaseModel):
    categoriaEventoId: int
    nombre: str

class Evento(BaseModel):
    eventoId: int
    nombre: str
    descripcion: str | None = None
    estado: str
    fechaCreacion: datetime
    usuario: UsuarioEvento
    categoriaEvento: CategoriaEventoEvento
    fechaInicio: datetime
    fechaFin: datetime
    fechaActualizacion: datetime | None = None
    usuarioActualizacionId: int | None = None