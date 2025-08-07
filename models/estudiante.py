from datetime import datetime
from pydantic import BaseModel


class UsuarioEstudiante(BaseModel):
    usuarioId: int
    nombre: str


class Estudiante(BaseModel):
    estudianteId: int
    nombres: str
    apellidos: str
    correo: str
    matricula: str | None = None
    estado: str
    usuarioCreacion: UsuarioEstudiante
    fechaCreacion: datetime
    usuarioActualizacion: UsuarioEstudiante | None = None
    fechaActualizacion: datetime | None = None