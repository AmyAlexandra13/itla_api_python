import logging
from datetime import datetime

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path, Query

from database.connection import get_connection
from database.estudiante import registrar_estudiante_pg, obtener_estudiante_pg, actualizar_estudiante_pg
from models.estudiante import Estudiante
from models.generico import ResponseData, ResponseList
from models.requests.actualizar_estudiante import ActualizarEstudianteRequest
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
                    "model": ResponseList[Estudiante]
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


@router.patch("/actualizar",
              summary='actualizarEstudiante',
              status_code=status.HTTP_204_NO_CONTENT)
def actualizar_estudiante(
        request: ActualizarEstudianteRequest = Body(),
        current_user: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        usuario_id = current_user['usuarioId']

        estudiante_id = request.estudianteId

        estudiantes_existentes = obtener_estudiante_pg(
            estudiante_id=estudiante_id,
            conexion=conexion
        )

        if not estudiantes_existentes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el estudiante especificado"
            )

        if isinstance(estudiantes_existentes, list):
            estudiante_actual = estudiantes_existentes[0]
        else:
            estudiante_actual = estudiantes_existentes['estudiantes'][0] if estudiantes_existentes[
                'estudiantes'] else None
            if not estudiante_actual:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontró el estudiante especificado"
                )
        if request.correo and str(request.correo) != estudiante_actual.correo:
            estudiantes_con_correo = obtener_estudiante_pg(
                correo=str(request.correo),
                conexion=conexion
            )

            if estudiantes_con_correo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otro estudiante registrado con este correo electrónico"
                )

        matricula_a_asignar = None
        estado_anterior = estudiante_actual.estado
        estado_nuevo = request.estado if request.estado else estado_anterior

        if (estado_nuevo == EstadoEstudiante.ACEPTADO and
                estado_anterior != EstadoEstudiante.ACEPTADO):
            anio_actual = datetime.now().year

            matricula_a_asignar = f"{anio_actual}-{estudiante_id}"

            logging.info(f"Generando matrícula automática: {matricula_a_asignar} para estudiante {estudiante_id}")

        estudiante_actualizado = actualizar_estudiante_pg(
            estudiante_id=estudiante_id,
            usuario_actualizacion_id=usuario_id,
            nombres=request.nombres,
            apellidos=request.apellidos,
            correo=request.correo,
            matricula=matricula_a_asignar,
            cedula=request.cedula,
            telefono=request.telefono,
            estado=request.estado,
            conexion=conexion
        )

        if not estudiante_actualizado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo actualizar el estudiante"
            )

        if request.estado and request.estado != estado_anterior:
            try:
                if request.estado == EstadoEstudiante.ACEPTADO:
                    email_enviado = email_service.enviar_email_admision_aceptada(
                        destinatario=str(request.correo) if request.correo else estudiante_actual.correo,
                        nombres=request.nombres if request.nombres else estudiante_actual.nombres,
                        apellidos=request.apellidos if request.apellidos else estudiante_actual.apellidos,
                        matricula=matricula_a_asignar
                    )

                    if email_enviado:
                        logging.info(f"Email de admisión aceptada enviado exitosamente a {estudiante_actual.correo}")
                    else:
                        logging.warning(f"No se pudo enviar el email de admisión aceptada a {estudiante_actual.correo}")

                elif request.estado == EstadoEstudiante.RECHAZADO:
                    email_enviado = email_service.enviar_email_admision_rechazada(
                        destinatario=str(request.correo) if request.correo else estudiante_actual.correo,
                        nombres=request.nombres if request.nombres else estudiante_actual.nombres,
                        apellidos=request.apellidos if request.apellidos else estudiante_actual.apellidos
                    )

                    if email_enviado:
                        logging.info(f"Email de admisión rechazada enviado exitosamente a {estudiante_actual.correo}")
                    else:
                        logging.warning(
                            f"No se pudo enviar el email de admisión rechazada a {estudiante_actual.correo}")

            except Exception as e:
                logging.error(f"Error al enviar email de notificación de admisión: {str(e)}")

        conexion.commit()

        return

    except HTTPException as e:
        logging.exception("Error controlado al actualizar estudiante")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado al actualizar estudiante")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()
