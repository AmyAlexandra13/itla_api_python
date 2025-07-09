print("✅ Router editorial.py activo")

from fastapi import APIRouter, HTTPException
from typing import List

from database import editorial
from models.requests.registrar_editorial import RegistrarEditorialRequest
from models.requests.actualizar_editorial import ActualizarEditorialRequest
from models.response.editorial import EditorialResponse

router = APIRouter(
    prefix="/editorial",
    tags=["Editoriales"]
)
@router.post("/registrar", response_model=int)
def registrar_editorial(data: RegistrarEditorialRequest):
    return editorial.crear_editorial(data)

@router.get("/", response_model=List[EditorialResponse])
def listar_editoriales():
    return editorial.listar_editoriales()

@router.get("/{editorial_id}", response_model=EditorialResponse)
def obtener_editorial(editorial_id: int):
    return editorial.obtener_editorial(editorial_id)

@router.patch("/actualizar/{editorial_id}", response_model=EditorialResponse)
def actualizar_editorial(editorial_id: int, data: ActualizarEditorialRequest):
    return editorial.actualizar_editorial(editorial_id, data)

@router.delete("/eliminar/{editorial_id}")
def eliminar_editorial(editorial_id: int):
    eliminadas = editorial.eliminar_editorial(editorial_id)
    if eliminadas == 0:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    return {"mensaje": "Editorial eliminada correctamente"}
