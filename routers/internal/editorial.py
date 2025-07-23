print("✅ Router editorial.py activo")

from fastapi import APIRouter, HTTPException
from typing import List

from database.editorial import (
    registrar_editorial_pg,
    obtener_editorial_pg,
    actualizar_editorial_pg,
    eliminar_editorial_pg
)

from models.requests.registrar_editorial import RegistrarEditorialRequest
from models.requests.actualizar_editorial import ActualizarEditorialRequest
from models.response.editorial import EditorialResponse

router = APIRouter(
    prefix="/editorial",
    tags=["editorial"]
)

@router.post("/", response_model=int)
def crear_editorial(data: RegistrarEditorialRequest):
    return registrar_editorial_pg(data.nombre, data.estado)

@router.get("/", response_model=List[EditorialResponse])
def listar_editoriales():
    return obtener_editorial_pg()

@router.get("/{editorial_id}", response_model=EditorialResponse)
def obtener_editorial(editorial_id: int):
    res = obtener_editorial_pg(editorial_id=editorial_id)
    if res:
        return res[0]
    else:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

@router.put("/{editorial_id}", response_model=EditorialResponse)
def actualizar_editorial(editorial_id: int, data: ActualizarEditorialRequest):
    return actualizar_editorial_pg(editorial_id, data.nombre, data.estado)

##@router.delete("/{editorial_id}", response_model=int)
#### return eliminar_editorial_pg(editorial_id)
