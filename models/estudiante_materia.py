from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class EstudianteOut(BaseModel):
    estudianteId: int
    nombres: str
    apellidos: str


class MateriaOut(BaseModel):
    materiaId: int
    nombre: str
    codigo: str


class CuatrimestreOut(BaseModel):
    cuatrimestreId: int
    periodo: str
    anio: int


class EstudianteMateria(BaseModel):
    estudianteMateriaId: int
    estudianteId: int
    materiaId: int
    cuatrimestreId: int
    estado: str
    calificacion: Decimal
    fechaCreacion: datetime
    fechaActualizacion: datetime | None = None
    estudiante: EstudianteOut
    materia: MateriaOut
    cuatrimestre: CuatrimestreOut