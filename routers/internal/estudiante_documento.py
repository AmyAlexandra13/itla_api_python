import logging
from io import BytesIO
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File, Form, Path, Query
from starlette.responses import StreamingResponse

from database.connection import get_connection
from database.estudiante import obtener_estudiante_pg
from database.estudiante_documento import (
    registrar_estudiante_documento_pg,
    obtener_estudiante_documento_pg,
    verificar_documento_existente_pg,
    verificar_documentos_completos_pg,
    obtener_content_estudiante_documento_pg,
    actualizar_estudiante_documento_pg
)
from models.estudiante_documento import EstudianteDocumento
from models.generico import ResponseData, ResponseList
from shared.constante import EstadoEstudiante, Rol, EstadoDocumento, SizeDocumento
from shared.email_service import email_service
from shared.permission import get_current_user

router = APIRouter(prefix="/estudiante-documento", tags=["Estudiante Documento"])


@router.post("/subir",
             responses={status.HTTP_201_CREATED: {"model": ResponseData[int]}},
             summary='subirDocumentoEstudiante', status_code=status.HTTP_201_CREATED)
async def subir_documento_estudiante(
        estudianteId: int = Form(...),
        tipoDocumento: str = Form(..., regex="^(CEDULA|ACTA_NACIMIENTO|RECORD_ESCUELA)$"),
        file: UploadFile = File(...),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        # Validar que el estudiante existe
        estudiantes = obtener_estudiante_pg(
            estudiante_id=estudianteId,
            conexion=conexion
        )

        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el estudiante especificado"
            )

        # El resultado puede ser lista o dict (paginado), manejamos ambos casos
        if isinstance(estudiantes, list):
            estudiante = estudiantes[0]
        else:
            estudiante = estudiantes['estudiantes'][0] if estudiantes['estudiantes'] else None
            if not estudiante:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontró el estudiante especificado"
                )

        # Validar que el estudiante esté en estado REGISTRADO
        if estudiante.estado != EstadoEstudiante.REGISTRADO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado del estudiante no permite subir documentos. El estudiante debe estar en estado REGISTRADO"
            )

        # Verificar si ya existe un documento del mismo tipo en estado VALIDO o PENDIENTE
        documento_existente = verificar_documento_existente_pg(
            estudiante_id=estudianteId,
            tipo_documento=tipoDocumento,
            conexion=conexion
        )

        if documento_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No puede subir un documento de tipo {tipoDocumento} debido a que ya lo ha cargado anteriormente"
            )

        # Validar el archivo
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar un archivo"
            )

        # Validar tipo de archivo (opcional - puedes agregar más validaciones)
        allowed_extensions = ['.pdf']
        file_extension = file.filename.lower().split('.')[-1]
        if f'.{file_extension}' not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de archivo no permitido. Solo se permiten PDF"
            )

        # Leer el contenido del archivo
        content = await file.read()

        # Validar tamaño del archivo
        if len(content) > SizeDocumento.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="El archivo excede los 10MB permitidos"
            )

        # Registrar el documento
        documento_id = registrar_estudiante_documento_pg(
            estudiante_id=estudianteId,
            tipo_documento=tipoDocumento,
            content=content,
            estado=EstadoDocumento.PENDIENTE,
            conexion=conexion
        )

        if not documento_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo registrar el documento"
            )

        # Verificar si ahora el estudiante tiene todos los documentos requeridos
        documentos_status = verificar_documentos_completos_pg(
            estudiante_id=estudianteId,
            conexion=conexion
        )

        if documentos_status['tiene_todos']:
            try:
                email_enviado = email_service.enviar_email_documentos_completos(
                    destinatario=estudiante.correo,
                    nombres=estudiante.nombres,
                    apellidos=estudiante.apellidos
                )

                if email_enviado:
                    logging.info(f"Email de documentos completos enviado exitosamente a {estudiante.correo}")
                else:
                    logging.warning(f"No se pudo enviar el email de documentos completos a {estudiante.correo}")

            except Exception as e:
                logging.error(f"Error al enviar email de documentos completos: {str(e)}")

        conexion.commit()

        return ResponseData[int](data=documento_id)

    except HTTPException as e:
        logging.exception("Error controlado al subir documento")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado al subir documento")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.get("/estudiante/{estudianteId}",
            responses={status.HTTP_200_OK: {"model": ResponseList[List[EstudianteDocumento]]}},
            summary='obtenerDocumentosEstudiante', status_code=status.HTTP_200_OK)
def obtener_documentos_estudiante(
        estudiante_id: int = Path(alias='estudianteId', description='ID del estudiante'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR)),
        estado: str | None = Query(
            None,
            description="Estado del documento",
            regex="^(PENDIENTE|VALIDO|RECHAZADO)$"
        )
):
    conexion = get_connection()

    try:
        # Validar que el estudiante existe
        estudiantes = obtener_estudiante_pg(
            estudiante_id=estudiante_id,
            conexion=conexion
        )

        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el estudiante especificado"
            )

        # Obtener documentos del estudiante
        documentos = obtener_estudiante_documento_pg(
            estudiante_id=estudiante_id,
            estado=estado,
            conexion=conexion
        )

        if not documentos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontraron documentos para el estudiante'
            )

        conexion.commit()

        return ResponseList(data=documentos)

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


@router.get("/{documentoId}/descargar",
            summary="Descargar documento del estudiante por ID",
            status_code=status.HTTP_200_OK)
def descargar_documento_estudiante(
        documentoId: int = Path(..., description="ID del documento"),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
) -> StreamingResponse:
    conexion = get_connection()

    try:
        # Verificar que el documento existe
        documentos = obtener_estudiante_documento_pg(
            estudiante_documento_id=documentoId,
            conexion=conexion
        )

        if not documentos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Documento no encontrado"
            )

        documento = documentos[0]

        # Obtener el contenido del documento
        content = obtener_content_estudiante_documento_pg(
            estudiante_documento_id=documentoId,
            conexion=conexion
        )

        if content is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contenido del documento no disponible"
            )

        file_like = BytesIO(content)

        # Generar nombre del archivo basado en el tipo de documento y estudiante
        estudiante_nombres = documento.estudiante['nombres'].replace(' ', '_')
        estudiante_apellidos = documento.estudiante['apellidos'].replace(' ', '_')
        tipo_doc = documento.tipoDocumento.lower()
        filename = f"{estudiante_nombres}_{estudiante_apellidos}_{tipo_doc}.pdf"

        return StreamingResponse(
            file_like,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException as e:
        logging.exception("Error esperado al descargar documento")
        raise e

    except Exception as e:
        logging.exception("Error inesperado al descargar documento")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.patch("/{documentoId}/estado",
              summary='actualizarEstadoDocumento', status_code=status.HTTP_204_NO_CONTENT)
def actualizar_estado_documento(
        documentoId: int = Path(..., description="ID del documento"),
        estado: str = Form(..., regex="^(PENDIENTE|VALIDO|RECHAZADO)$"),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
):
    conexion = get_connection()

    try:
        # Verificar que el documento existe
        documentos = obtener_estudiante_documento_pg(
            estudiante_documento_id=documentoId,
            conexion=conexion
        )

        if not documentos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No se encontró el documento para actualizar'
            )

        # Actualizar el estado del documento
        documento_actualizado = actualizar_estudiante_documento_pg(
            estudiante_documento_id=documentoId,
            estado=estado,
            conexion=conexion
        )

        if not documento_actualizado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No se pudo actualizar el estado del documento'
            )

        conexion.commit()

        return

    except HTTPException as e:
        logging.exception("Error controlado al actualizar estado del documento")
        conexion.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.exception("Ocurrió un error inesperado al actualizar estado del documento")
        conexion.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()


@router.get("/estudiante/{matricula}/descargar",
            summary="Descargar todos los documentos del estudiante en un ZIP",
            status_code=status.HTTP_200_OK)
def descargar_documentos_estudiante(
        matricula: str = Path(alias='matricula', description='Matricula del estudiante'),
        _: dict = Depends(get_current_user(Rol.ADMINISTRADOR))
) -> StreamingResponse:
    import zipfile

    conexion = get_connection()

    try:
        # Verificar que el estudiante existe
        estudiantes = obtener_estudiante_pg(
            matricula=matricula,
            conexion=conexion
        )

        if not estudiantes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el estudiante especificado"
            )

        # El resultado puede ser lista o dict (paginado), manejamos ambos casos
        if isinstance(estudiantes, list):
            estudiante = estudiantes[0]
        else:
            estudiante = estudiantes['estudiantes'][0] if estudiantes['estudiantes'] else None
            if not estudiante:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontró el estudiante especificado"
                )

        estudiante_id = estudiante.estudianteId

        # Obtener todos los documentos del estudiante
        documentos = obtener_estudiante_documento_pg(
            estudiante_id=estudiante_id,
            conexion=conexion
        )

        if not documentos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El estudiante no tiene documentos registrados"
            )

        # Crear el ZIP directamente en memoria
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for documento in documentos:
                # Obtener el contenido del documento
                content = obtener_content_estudiante_documento_pg(
                    estudiante_documento_id=documento.estudianteDocumentoId,
                    conexion=conexion
                )

                if content is not None:
                    # Generar nombre del archivo
                    tipo_doc = documento.tipoDocumento.lower()
                    estado_doc = documento.estado.lower()
                    fecha_creacion = documento.fechaCreacion.replace(':', '-').replace(' ', '_')
                    filename = f"{tipo_doc}_{estado_doc}_{fecha_creacion}.pdf"

                    # Agregar el archivo al ZIP
                    zip_file.writestr(filename, content)

        # Posicionar el cursor al inicio del buffer
        zip_buffer.seek(0)

        # Generar nombre del archivo ZIP
        estudiante_nombres = estudiante.nombres.replace(' ', '_')
        estudiante_apellidos = estudiante.apellidos.replace(' ', '_')
        zip_filename = f"documentos_{estudiante_nombres}_{estudiante_apellidos}.zip"

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={zip_filename}"}
        )

    except HTTPException as e:
        logging.exception("Error esperado al descargar documentos del estudiante")
        raise e

    except Exception as e:
        logging.exception("Error inesperado al descargar documentos del estudiante")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        conexion.close()
