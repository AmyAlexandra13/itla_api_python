from typing import List

from pydantic import BaseModel

from models.paginacion import PaginacionUNICDA


class InstitucionExternaUnicda(BaseModel):
    id: int
    nombre: str


class EstudianteUNICDA(BaseModel):
    """Modelo para estudiantes de UNICDA"""
    id: int
    institucionExternaId: int
    nombre: str
    apellido: str
    cedula: str
    convalidado: bool
    matricula: str
    institucionExterna: InstitucionExternaUnicda | None = None


class EstudiantesUNICDAPaginadoResponse(BaseModel):
    pagination: PaginacionUNICDA
    data: List[EstudianteUNICDA]