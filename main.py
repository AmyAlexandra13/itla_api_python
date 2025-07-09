import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers internos
from routers.internal import auth, categoria_evento, evento, editorial

# Inicializar logging
logging.basicConfig(level=logging.DEBUG)

# Inicializar app FastAPI
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes especificar frontend aquí
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/internal")
app.include_router(categoria_evento.router, prefix="/internal")
app.include_router(evento.router, prefix="/internal")
app.include_router(editorial.router, prefix="/internal")

# print("✅ Router editorial.py activo")  # Esto debe verse al ejecutar el servidor

# Ejecutar Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
