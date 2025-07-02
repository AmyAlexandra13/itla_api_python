from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from database.usuario import buscar_rol_usuario_pg

SECRET_KEY = "supersecreto123"  # Mismo que el usado al firmar el token
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(rol_id: int):
    def dependency(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

        permissions_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene los permisos necesarios",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario_id = payload.get("sub")

            if usuario_id is None:
                raise credentials_exception

            # Validar que el usuario tenga el rol
            usuario_rol = buscar_rol_usuario_pg(usuario_id, rol_id)

            if not usuario_rol:
                raise permissions_exception

            return usuario_rol

        except JWTError:
            raise credentials_exception

    return dependency  # <-- retornas la función interior