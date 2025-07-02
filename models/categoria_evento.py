from pydantic import BaseModel

class UsuarioCategoriaEvento(BaseModel):
    usuarioId: int
    nombre: str

class CategoriaEvento(BaseModel):
    categoriaEventoId: int
    nombre: str
    estado: str
    fechaCreacion: str
    usuario: UsuarioCategoriaEvento
    fechaActualizacion: str | None = None
    usuarioActualizacionId: int | None = None