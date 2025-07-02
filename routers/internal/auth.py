import logging
from http import HTTPStatus

from fastapi import APIRouter, Body, HTTPException, status

from database.connection import get_connection
from database.usuario import registrar_usuario_pg, obtener_usuario_pg
from models.generico import ResponseData
from models.requests.login import LoginUsuario
from models.requests.registrar_usuario import RegistrarUsuarioModel
from models.response.login_response import LoginResponseModel
from shared.constante import Estado
from shared.utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarUsuario', status_code=status.HTTP_201_CREATED)
def registrar(request: RegistrarUsuarioModel = Body()):
    conexion = get_connection()

    try:

        logging.info('Buscando usuario con ese correo')

        usuario_con_correo = obtener_usuario_pg(request.correo, conexion)

        if usuario_con_correo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya se encuentra registrado"
            )

        hashed_clave = hash_password(request.clave)

        usuario_id = registrar_usuario_pg(
            nombre=request.nombre,
            correo=request.correo,
            clave=hashed_clave,
            estado=Estado.ACTIVO,
            rol_id=request.rolId,
            conexion=conexion
        )

        if not usuario_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="No se pudo registrar el usuario"
            )

        conexion.commit()

        return ResponseData[int](data=usuario_id)


    except HTTPException as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e.detail)


    except Exception as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


    finally:
        conexion.close()


@router.post("/login",
             responses={status.HTTP_200_OK: {"model": ResponseData[LoginResponseModel]}},
             summary='logearUsuario', status_code=status.HTTP_200_OK)
def login(request: LoginUsuario = Body()):

    conexion = get_connection()

    try:

        logging.info('Buscando usuario con ese correo')

        usuario = obtener_usuario_pg(request.correo, conexion)

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No existe un usuario con ese correo"
            )

        hashed_clave_usuario = usuario['clave']

        usuario_id = usuario['usuarioId']

        password_vertified = verify_password(request.clave, hashed_clave_usuario)

        if not password_vertified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Credenciales inválidas"
            )

        token = create_access_token({"sub": str(usuario_id)})

        login_response = LoginResponseModel(
            accessToken=token,
            tokenType="bearer"
        )

        conexion.commit()

        return ResponseData[LoginResponseModel](data=login_response)

    except HTTPException as e:

        logging.exception("Ocurrió un error inesperado")

        conexion.rollback()

        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:

        logging.exception("Ocurrió un error inesperado")

        logging.warning(e)

        conexion.rollback()

        raise e

    finally:
        conexion.close()
