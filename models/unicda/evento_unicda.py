# Crear archivo models/unicda/evento.py
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class EventoUNICDA(BaseModel):
    """Modelo para eventos de UNICDA"""
    id: int
    categoriaEventoId: int
    titulo: str
    descripcion: str
    fecha: datetime


class PaginacionUNICDA(BaseModel):
    """Modelo para paginación de UNICDA"""
    pages: int
    records: int
    currentPage: int
    prevPage: int
    nextPage: int


class EventosUNICDAPaginadoResponse(BaseModel):
    """Modelo para respuesta paginada de eventos de UNICDA"""
    pagination: PaginacionUNICDA
    data: List[EventoUNICDA]


class EventosUNICDARequest(BaseModel):
    """Modelo para petición de eventos de UNICDA"""
    page: Optional[int] = 1
    pageSize: Optional[int] = 10
    categoriaEventoId: Optional[int] = None
    fechaInicio: Optional[datetime] = None
    fechaFin: Optional[datetime] = None