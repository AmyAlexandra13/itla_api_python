from datetime import datetime, timedelta
from typing import Optional, Any, List, Dict

import psycopg2
from jose import jwt
from passlib.context import CryptContext

from database.connection import get_connection


def snake_to_camel(snake_str: str) -> str:
    parts = snake_str.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def snake_to_camel_dict(row: dict) -> dict:
    return {snake_to_camel(k): v for k, v in row.items()}


def execute_query(
        query: str,
        values=None,
        conn: Optional[psycopg2.extensions.connection] = None
) -> Optional[List[Dict[str, Any]]]:
    if values is None:
        values = []
    close_connection = False

    if conn is None:
        conn = get_connection()
        close_connection = True

    cursor = conn.cursor()
    result = None

    try:
        cursor.execute(query, values)

        if cursor.description:  # es un SELECT
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            if rows is None:
                return None

            result = [
                snake_to_camel_dict(dict(zip(columns, row)))
                for row in rows
            ]
        elif close_connection:
            conn.commit()

    except Exception as e:
        if close_connection:
            conn.rollback()
        raise e
    finally:
        cursor.close()
        if close_connection:
            conn.close()

    return result


def formartear_secuencia_insertar_sql(sql, fields) -> str:
    query = f"{sql} ({', '.join(fields)}) values ({', '.join(['%s'] * len(fields))})"

    return query


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    secret_key = "supersecreto123"

    algorithm = "HS256"

    access_token_expire_minutes = 60

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


from datetime import datetime


def validar_fechas(fecha_inicio: datetime, fecha_fin: datetime) -> dict:
    errores = []
    ahora = datetime.now()

    if fecha_inicio < ahora:
        errores.append("La fecha de inicio debe ser mayor o igual a la fecha actual.")

    if fecha_fin <= fecha_inicio:
        errores.append("La fecha de fin debe ser mayor que la fecha de inicio.")

    return {
        "valido": len(errores) == 0,
        "errores": errores
    }

