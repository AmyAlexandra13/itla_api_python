# security/security.py

from datetime import datetime, timedelta
from typing import Dict, Any, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.rol import Rol

# --- Configuración de Seguridad ---
SECRET_KEY = "tu_super_secreto_aqui_cambialo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/internal/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Funciones de Seguridad ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(required_roles: List[Rol] = None):
    def _get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            roles: List[str] = payload.get("roles", [])
            if user_id is None:
                raise credentials_exception

            if required_roles:
                is_authorized = any(role in [r.value for r in required_roles] for role in roles)
                if not is_authorized:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permiso para realizar esta acción",
                    )

            return {"usuarioId": int(user_id), "roles": roles}
        except JWTError:
            raise credentials_exception

    return _get_current_user
