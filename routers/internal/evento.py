# routers/internal/evento.py
from fastapi import APIRouter, Depends
from database.connection import get_connection
from database.evento import obtener_evento_pg

router = APIRouter()

@router.get("/")
def obtener_eventos(conn = Depends(get_connection)):
    # Ahora sí llamamos a la función que busca en la base de datos
    eventos = obtener_evento_pg(conexion=conn)
    return {"data": eventos}