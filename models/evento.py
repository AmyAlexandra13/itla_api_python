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
    fechaCreacion: str
    usuario: UsuarioEvento
    categoriaEvento: CategoriaEventoEvento
    fechaInicio: str
    fechaFin: str
    fechaActualizacion: str | None = None
    usuarioActualizacionId: int | None = None