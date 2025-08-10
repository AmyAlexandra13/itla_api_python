import logging
from typing import List

from fastapi import APIRouter, status, Body, Depends, HTTPException, Path, Query

from database.connection import get_connection
from database.cuatrimestre import obtener_cuatrimestre_pg
from database.estudiante import obtener_estudiante_pg
from database.estudiante_materia import (
    registrar_estudiante_materia_pg,
    obtener_estudiante_materia_pg,
    actualizar_estudiante_materia_pg,
    verificar_estudiante_materia_existente_pg
)
from database.materia import obtener_materia_pg
from models.estudiante_materia import EstudianteMateria
from models.generico import ResponseData, ResponseList
from models.paginacion import ResponsePaginado
from models.requests.actualizar_estudiante_materia import ActualizarEstudianteMateriaRequest
from models.requests.registrar_estudiante_materia import RegistrarEstudianteMateriaRequest
from shared.constante import Estado, Rol, EstadoEstudiante, EstadoEstudianteMateria, Calificacion
from shared.permission import get_current_user

router = APIRouter(prefix="/estudiante-materia", tags=["Estudiante Materia"])


@router.post("/registrar",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='registrarEstudianteMateria', status_code=status.HTTP_201_CREATED)
def registrar_estudiante_materia(
        request: RegistrarEstudianteMateriaRequest = Body(),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        estudiantes = obtener_estudiante_pg(
            estudiante_id=request.estudianteId,
            estado=EstadoEstudiante.ACEPTADO,
            conexion=conexion
        )

        estado_req = request.estado

        calificacion = None if request.estado == EstadoEstudianteMateria.RETIRADA else request.calificacion

        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el estudiante especificado o no esta aceptado en la institucion"
            )

        if estado_req == EstadoEstudianteMateria.REPROBADA and calificacion is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe indicar la nota reprobada"
            )

        if estado_req == EstadoEstudianteMateria.APROBADA and calificacion is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe indicar la aprobada"
            )

        if estado_req == EstadoEstudianteMateria.REPROBADA and calificacion >= Calificacion.MINIMO_APROBACION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las calificaciones reprobadas esta por debajo de 70"
            )

        if estado_req == EstadoEstudianteMateria.APROBADA and calificacion < Calificacion.MINIMO_APROBACION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las calificaciones aprobadas estan por encima o igual a 70"
            )

        estudiante = estudiantes[0]

        estudiante_id = estudiante.estudianteId

        materia_id = request.materiaId

        materias = obtener_materia_pg(
            materia_id=request.materiaId,
            estado=Estado.ACTIVO,
            conexion=conexion
        )

        if not materias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró la materia especificada o está inactiva"
            )

        cuatrimestres = obtener_cuatrimestre_pg(
            cuatrimestre_id=request.cuatrimestreId,
            estado=Estado.ACTIVO,
            conexion=conexion
        )

        if not cuatrimestres:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el cuatrimestre especificado o está inactivo"
            )

        # Verificar que no existe ya un registro para este estudiante, materia y cuatrimestre
        existe_registro = verificar_estudiante_materia_existente_pg(
            estudiante_id=request.estudianteId,
            materia_id=request.materiaId,
            cuatrimestre_id=request.cuatrimestreId,
            conexion=conexion
        )

        if existe_registro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un registro para este estudiante en esta materia y cuatrimestre"
            )

        materia_anteriormente_aprobada = obtener_estudiante_materia_pg(
            estudiante_id=estudiante_id,
            materia_id=materia_id,
            estado=EstadoEstudianteMateria.APROBADA
        )

        if materia_anteriormente_aprobada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta materia ha sido anteriormente aprobada"
            )
        # Registrar el estudiante-materia
        estudiante_materia_id = registrar_estudiante_materia_pg(
            estudiante_id=request.estudianteId,
            materia_id=request.materiaId,
            cuatrimestre_id=request.cuatrimestreId,
            estado=request.estado,
            calificacion=calificacion,
            conexion=conexion
        )

        if not estudiante_materia_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo registrar la materia de este estudiante"
            )

        conexion.commit()

        return ResponseData[int](data=estudiante_materia_id)

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


@router.get("/",
            responses={
                status.HTTP_200_OK: {
                    "model": ResponsePaginado[EstudianteMateria]
                }
            },
            summary='obtenerEstudianteMaterias', status_code=status.HTTP_200_OK)
def obtener_estudiante_materias(
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        estudianteId: int | None = Query(
            None,
            description="ID del estudiante",
            ge=1
        ),
        materiaId: int | None = Query(
            None,
            description="ID de la materia",
            ge=1
        ),
        cuatrimestreId: int | None = Query(
            None,
            description="ID del cuatrimestre",
            ge=1
        ),
        estado: str | None = Query(
            None,
            description="Estado de la materia del estudiante",
            regex="^(RETIRADA|APROBADA|REPROBADA)$"
        )
):
    conexion = get_connection()

    try:
        resultado = obtener_estudiante_materia_pg(
            estudiante_id=estudianteId,
            materia_id=materiaId,
            cuatrimestre_id=cuatrimestreId,
            estado=estado,
            conexion=conexion
        )

        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron registros de estudiante-materia'
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


@router.get("/{estudianteMateriaId}",
            responses={status.HTTP_200_OK: {"model": ResponseData[EstudianteMateria]}},
            summary='obtenerEstudianteMateriaPorId', status_code=status.HTTP_200_OK)
def obtener_estudiante_materia_por_id(
        estudiante_materia_id: int = Path(alias='estudianteMateriaId',
                                          description='ID del registro estudiante-materia'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        estudiante_materias = obtener_estudiante_materia_pg(
            estudiante_materia_id=estudiante_materia_id,
            conexion=conexion
        )

        if not estudiante_materias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el registro de estudiante-materia'
            )

        estudiante_materia = estudiante_materias[0]

        conexion.commit()

        return ResponseData(data=estudiante_materia)

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
              summary='actualizarEstudianteMateria', status_code=status.HTTP_204_NO_CONTENT)
def actualizar_estudiante_materia(
        request: ActualizarEstudianteMateriaRequest = Body(),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        estudiante_materia_id = request.estudianteMateriaId

        # Verificar que el registro existe
        estudiante_materias = obtener_estudiante_materia_pg(
            estudiante_materia_id=estudiante_materia_id,
            conexion=conexion
        )

        if not estudiante_materias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el registro de estudiante-materia para actualizar'
            )

        # Validar que al menos un campo se va a actualizar
        if request.estado is None and request.calificacion is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se encontró ningún campo para actualizar'
            )

        estado_req = request.estado

        calificacion = None if request.estado == EstadoEstudianteMateria.RETIRADA else request.calificacion

        if calificacion:

            if estado_req == EstadoEstudianteMateria.REPROBADA and calificacion >= Calificacion.MINIMO_APROBACION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Las calificaciones reprobadas esta por debajo de 70"
                )

            if estado_req == EstadoEstudianteMateria.APROBADA and calificacion < Calificacion.MINIMO_APROBACION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Las calificaciones aprobadas estan por encima o igual a 70"
                )

        estudiante_materia_actualizado = actualizar_estudiante_materia_pg(
            estudiante_materia_id=estudiante_materia_id,
            estado=request.estado,
            calificacion=request.calificacion,
            conexion=conexion
        )

        if not estudiante_materia_actualizado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se pudo actualizar el registro de estudiante-materia'
            )

        conexion.commit()

        return

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


@router.get("/estudiante/{estudianteId}/historial",
            responses={
                status.HTTP_200_OK: {
                    "model": ResponseList[List[EstudianteMateria]]
                }
            },
            summary='obtenerHistorialAcademicoEstudiante', status_code=status.HTTP_200_OK)
def obtener_historial_academico_estudiante(
        estudiante_id: int = Path(alias='estudianteId', description='ID del estudiante'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        estado: str | None = Query(
            None,
            description="Estado de las materias",
            regex="^(RETIRADA|APROBADA|REPROBADA)$"
        )
):
    """
    Endpoint adicional para obtener el historial académico completo de un estudiante
    """
    conexion = get_connection()

    try:
        # Verificar que el estudiante existe
        estudiantes = obtener_estudiante_pg(
            estudiante_id=estudiante_id,
            conexion=conexion
        )

        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el estudiante especificado"
            )

        # Obtener todas las materias del estudiante
        estudiante_materias = obtener_estudiante_materia_pg(
            estudiante_id=estudiante_id,
            estado=estado,
            conexion=conexion
        )

        if not estudiante_materias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró historial académico para el estudiante'
            )

        conexion.commit()

        return ResponseList(data=estudiante_materias)

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
