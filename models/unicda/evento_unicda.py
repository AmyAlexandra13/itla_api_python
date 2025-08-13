# Crear archivo models/unicda/evento.py
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from models.paginacion import PaginacionUNICDA


class CategoriaEventoUnicda(BaseModel):
    id: int
    nombre: str

class EventoUNICDA(BaseModel):
    id: int
    categoriaEventoId: int
    titulo: str
    descripcion: str
    fecha: datetime
    categoriaEvento: CategoriaEventoUnicda


class EventosUNICDAPaginadoResponse(BaseModel):
    pagination: PaginacionUNICDA
    data: List[EventoUNICDA]


class EventosUNICDARequest(BaseModel):
    page: Optional[int] = 1
    pageSize: Optional[int] = 10
    categoriaEventoId: Optional[int] = None
    fechaInicio: Optional[datetime] = None
    fechaFin: Optional[datetime] = None
