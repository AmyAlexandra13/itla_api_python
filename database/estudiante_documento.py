import psycopg2
from models.estudiante_documento import EstudianteDocumento
from shared.utils import formartear_secuencia_insertar_sql, execute_query


def registrar_estudiante_documento_pg(
        estudiante_id: int,
        tipo_documento: str,
        content: bytes,
        estado: str,
        conexion: psycopg2.extensions.connection | None = None
):
    fields = [
        'estudiante_id',
        'tipo_documento',
        'content',
        'estado'
    ]

    values = [
        estudiante_id,
        tipo_documento,
        psycopg2.Binary(content),
        estado
    ]

    sql = "insert into estudiante_documento"

    query = formartear_secuencia_insertar_sql(sql, fields)

    query += " returning estudiante_documento_id;"

    results = execute_query(query, values, conn=conexion)

    return next((item['estudianteDocumentoId'] for item in results), None)


def query_seleccionar_datos_estudiante_documento():
    return '''
        select 
            ed.estudiante_documento_id,
            ed.estudiante_id,
            ed.tipo_documento,
            ed.estado,
            to_char(ed.fecha_creacion, 'DD-MM-YYYY HH24:MI:SS') as fecha_creacion,
            to_char(ed.fecha_actualizacion, 'DD-MM-YYYY HH24:MI:SS') as fecha_actualizacion,
            json_build_object(
                'estudianteId', e.estudiante_id,
                'nombres', e.nombres,
                'apellidos', e.apellidos,
                'correo', e.correo
            ) as estudiante
        from estudiante_documento ed
        join estudiante e on ed.estudiante_id = e.estudiante_id
    '''


def obtener_estudiante_documento_pg(
        estudiante_documento_id: int | None = None,
        estudiante_id: int | None = None,
        tipo_documento: str | None = None,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = query_seleccionar_datos_estudiante_documento()

    where_exprss = []
    values = []

    if estudiante_documento_id is not None:
        where_exprss.append("ed.estudiante_documento_id = %s")
        values.append(estudiante_documento_id)

    if estudiante_id is not None:
        where_exprss.append("ed.estudiante_id = %s")
        values.append(estudiante_id)

    if tipo_documento is not None:
        where_exprss.append("ed.tipo_documento = %s")
        values.append(tipo_documento)

    if estado is not None:
        where_exprss.append("ed.estado = %s")
        values.append(estado)

    if where_exprss:
        sql += " where " + " and ".join(where_exprss)

    sql += " order by ed.fecha_creacion desc;"

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    items = [EstudianteDocumento(**item) for item in results]

    return items


def verificar_documento_existente_pg(
        estudiante_id: int,
        tipo_documento: str,
        conexion: psycopg2.extensions.connection | None = None
):
    """
    Verifica si existe un documento del estudiante con el tipo específico
    y en estado VALIDO o PENDIENTE
    """
    sql = '''
        select count(*) as total
        from estudiante_documento
        where estudiante_id = %s 
          and tipo_documento = %s 
          and estado in ('VALIDO', 'PENDIENTE');
    '''

    values = [estudiante_id, tipo_documento]

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return False

    return results[0]['total'] > 0


def obtener_content_estudiante_documento_pg(
        estudiante_documento_id: int,
        conexion: psycopg2.extensions.connection | None = None
):
    """
    Obtiene el contenido binario de un documento del estudiante
    """
    sql = '''
        SELECT content
        FROM estudiante_documento
        WHERE estudiante_documento_id = %s;
    '''

    values = [estudiante_documento_id]

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return None

    return results[0]['content']


def verificar_documentos_completos_pg(
        estudiante_id: int,
        conexion: psycopg2.extensions.connection | None = None
):
    """
    Verifica si el estudiante tiene todos los documentos requeridos subidos
    (CEDULA, ACTA_NACIMIENTO, RECORD_ESCUELA) en cualquier estado
    """
    sql = '''
        select 
            count(distinct tipo_documento) as documentos_subidos,
            array_agg(distinct tipo_documento) as tipos_subidos
        from estudiante_documento
        where estudiante_id = %s 
          and tipo_documento in ('CEDULA', 'ACTA_NACIMIENTO', 'RECORD_ESCUELA');
    '''

    values = [estudiante_id]

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return {
            'tiene_todos': False,
            'documentos_subidos': 0,
            'tipos_subidos': []
        }

    result = results[0]
    documentos_subidos = result['documentosSubidos'] or 0
    tipos_subidos = result['tiposSubidos'] or []

    # Necesita tener los 3 tipos de documentos
    documentos_requeridos = 3
    tiene_todos = documentos_subidos == documentos_requeridos

    return {
        'tiene_todos': tiene_todos,
        'documentos_subidos': documentos_subidos,
        'tipos_subidos': tipos_subidos
    }


def actualizar_estudiante_documento_pg(
        estudiante_documento_id: int,
        estado: str | None = None,
        conexion: psycopg2.extensions.connection | None = None
):
    """
    Actualiza el estado de un documento del estudiante
    """
    fields = []
    values = []

    if estado is not None:
        fields.append("estado = %s")
        values.append(estado)

    if not fields:
        return None

    values.append(estudiante_documento_id)

    sql = """
          update estudiante_documento 
          set fecha_actualizacion = (now() at time zone 'EDT'),
          """

    sql += ", ".join(fields)

    sql += " where estudiante_documento_id = %s"

    sql += " returning estudiante_documento_id;"

    documento_actualizado = execute_query(sql, values, conn=conexion)

    if not documento_actualizado:
        return None

    return documento_actualizado[0]['estudianteDocumentoId']

def verificar_documentos_validos_completos_pg(
        estudiante_id: int,
        conexion: psycopg2.extensions.connection | None = None
):
    sql = '''
        select 
            count(distinct tipo_documento) as documentos_validos,
            array_agg(distinct tipo_documento) as tipos_validos
        from estudiante_documento
        where estudiante_id = %s 
          and estado = 'VALIDO'
          and tipo_documento in ('CEDULA', 'ACTA_NACIMIENTO', 'RECORD_ESCUELA');
    '''

    values = [estudiante_id]

    results = execute_query(sql, values, conn=conexion)

    if not results:
        return {
            'tiene_todos_validos': False,
            'documentos_validos': 0,
            'tipos_validos': []
        }

    result = results[0]
    documentos_validos = result['documentosValidos'] or 0
    tipos_validos = result['tiposValidos'] or []

    documentos_requeridos = 3
    tiene_todos_validos = documentos_validos == documentos_requeridos

    return {
        'tiene_todos_validos': tiene_todos_validos,
        'documentos_validos': documentos_validos,
        'tipos_validos': tipos_validos
    }