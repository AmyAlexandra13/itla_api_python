import uvicorn
from fastapi import FastAPI
from routers.internal import auth, categoria_evento
import logging


app = FastAPI()

logging.basicConfig(level=logging.DEBUG)


app.include_router(auth.router, prefix="/internal")
app.include_router(categoria_evento.router, prefix='/internal')

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)