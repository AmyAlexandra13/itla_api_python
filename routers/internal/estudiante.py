import logging

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path, Query

from database.connection import get_connection
from database.estudiante import registrar_estudiante_pg, obtener_estudiante_pg
from models.estudiante import Estudiante
from models.generico import ResponseData, ResponseList
from models.paginacion import ResponsePaginado
from models.requests.registrar_estudiante import RegistrarEstudianteRequest
from shared.constante import EstadoEstudiante, Rol
from shared.email_service import email_service
from shared.permission import get_current_user

router = APIRouter(prefix="/estudiante", tags=["Estudiante"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarEstudiante', status_code=status.HTTP_201_CREATED)
def registrar_estudiante(
        request: RegistrarEstudianteRequest = Body(),
        current_user: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        # Verificar que no exista un estudiante con el mismo correo

        correo = str(request.correo)

        estudiantes_existentes = obtener_estudiante_pg(
            correo=correo,
            conexion=conexion
        )

        if estudiantes_existentes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un estudiante registrado con este correo electrónico"
            )

        usuario_id = current_user['usuarioId']

        estudiante_id = registrar_estudiante_pg(
            nombres=request.nombres,
            apellidos=request.apellidos,
            correo=request.correo,
            cedula=request.cedula,
            telefono=request.telefono,
            estado=EstadoEstudiante.REGISTRADO,
            usuario_creacion_id=usuario_id,
            conexion=conexion
        )

        if not estudiante_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo registrar el estudiante"
            )

        try:
            email_enviado = email_service.enviar_email_registro_estudiante(
                destinatario=request.correo,
                nombres=request.nombres,
                apellidos=request.apellidos
            )

            if email_enviado:
                logging.info(f"Email de registro enviado exitosamente a {request.correo}")
            else:
                logging.warning(f"No se pudo enviar el email de registro a {request.correo}")

        except Exception as e:
            logging.error(f"Error al enviar email de registro: {str(e)}")

        conexion.commit()

        return ResponseData[int](data=estudiante_id)

    except HTTPException as e:
        logging.exception("Error controlado en registro de estudiante")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado en registro de estudiante")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.get("/",
            responses={
                status.HTTP_200_OK: {
                    "model": ResponsePaginado[Estudiante]
                }
            },
            summary='obtenerEstudiantes', status_code=status.HTTP_200_OK)
def obtener_estudiantes(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        estado: str | None = Query(
            None,
            description="Estado del estudiante",
            regex="^(REGISTRADO|PENDIENTE_DOCUMENTO|ACEPTADO|RECHAZADO|GRADUADO)$"
        ),
        matricula: str | None = Query(
            default=None,
            description='Matricula del estudiante'
        ),
        correo: str | None = Query(
            default=None,
            description='Correo del estudiante'
        )
):
    conexion = get_connection()

    try:
        resultado = obtener_estudiante_pg(
            estado=estado,
            correo=correo,
            matricula=matricula,
            conexion=conexion
        )

        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron estudiantes'
            )

        conexion.commit()

        return ResponseList(data=resultado)
    except HTTPException as e:
        logging.exception("Error controlado")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.get("/{estudianteId}",
            responses={status.HTTP_200_OK: {"model": ResponseData[Estudiante]}},
            summary='obtenerEstudiantePorId', status_code=status.HTTP_200_OK)
def obtener_estudiante_por_id(
        estudiante_id: int = Path(alias='estudianteId', description='ID del estudiante'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        estudiantes = obtener_estudiante_pg(
            estudiante_id=estudiante_id,
            conexion=conexion
        )

        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el estudiante'
            )

        # El resultado será una lista cuando no hay paginación
        if isinstance(estudiantes, list):
            estudiante = estudiantes[0]
        else:
            # Si por alguna razón llega como dict, manejarlo
            estudiante = estudiantes['estudiantes'][0] if estudiantes['estudiantes'] else None
            if not estudiante:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='No se encontró el estudiante'
                )

        conexion.commit()

        return ResponseData(data=estudiante)

    except HTTPException as e:
        logging.exception("Error controlado")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.get("/correo/{correo}",
            responses={status.HTTP_200_OK: {"model": ResponseData[Estudiante]}},
            summary='obtenerEstudiantePorCorreo', status_code=status.HTTP_200_OK)
def obtener_estudiante_por_correo(
        correo: str = Path(description='Correo del estudiante'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        estudiantes = obtener_estudiante_pg(
            correo=correo,
            conexion=conexion
        )

        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró un estudiante con ese correo'
            )

        # El resultado será una lista cuando no hay paginación
        if isinstance(estudiantes, list):
            estudiante = estudiantes[0]
        else:
            # Si por alguna razón llega como dict, manejarlo
            estudiante = estudiantes['estudiantes'][0] if estudiantes['estudiantes'] else None
            if not estudiante:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='No se encontró un estudiante con ese correo'
                )

        conexion.commit()

        return ResponseData(data=estudiante)

    except HTTPException as e:
        logging.exception("Error controlado")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()
