import psycopg2
from fastapi import HTTPException

def get_connection():
    try:
        return psycopg2.connect(
            host="localhost",
            database="itla_api_db",
            user="postgres",
            password="admin",
            port=5432
        )
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        raise HTTPException(status_code=500, detail=str(e))
