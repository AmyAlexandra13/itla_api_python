import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Importamos todos los routers que vamos a usar
from routers.internal import auth, categoria_evento, evento
from security.security import get_current_user

app = FastAPI(title="ITLA Events API")

# --- CORRECCIÓN DE CORS AQUÍ ---
# Esta configuración es más explícita y permite las peticiones
# desde archivos locales (origin 'null') y cualquier otro origen.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # Permitimos todos los orígenes y 'null' para archivos locales
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# --- INCLUIMOS TODOS LOS ROUTERS ---
# Autenticación
app.include_router(auth.router, prefix='/internal/auth', tags=['Autenticación'])

# Categoría Evento
app.include_router(
    categoria_evento.router,
    prefix='/internal/categoria-evento',
    tags=['Categoría Evento'],
    dependencies=[Depends(get_current_user)]
)

# Evento
app.include_router(
    evento.router,
    prefix='/internal/evento',
    tags=['Evento'],
    #dependencies=[Depends(get_current_user)]
)

@app.get("/", tags=['Health Check'])
def root():
    return {"message": "API de Eventos ITLA está funcionando."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080) # Usamos el puerto 8080