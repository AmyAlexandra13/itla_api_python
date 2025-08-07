import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.internal import auth, categoria_evento, evento, libro, editorial, programa_academico, materia, estudiante
import logging


app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos, incluyendo OPTIONS
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/internal")
app.include_router(categoria_evento.router, prefix='/internal')
app.include_router(evento.router, prefix='/internal')

app.include_router(libro.router, prefix='/internal')
app.include_router(editorial.router, prefix='/internal')
app.include_router(programa_academico.router, prefix='/internal')
app.include_router(materia.router, prefix='/internal')
app.include_router(estudiante.router, prefix='/internal')

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)