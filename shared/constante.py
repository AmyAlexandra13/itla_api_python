class Estado:
    ACTIVO = 'AC'
    INACTIVO = 'IN'


class Rol:
    ADMINISTRADOR = 1
    USUARIO = 2
    CLIENTE = 3

class SizeLibro:
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

class EstadoEstudiante:
    REGISTRADO = 'REGISTRADO'
    PENDIENTE_DOCUMENTO = 'PENDIENTE_DOCUMENTO'
    PENDIENTE_RESPUESTA = 'PENDIENTE_RESPUESTA'
    ACEPTADO = 'ACEPTADO'
    RECHAZADO = 'RECHAZADO'
    GRADUADO = 'GRADUADO'


class TipoDocumento:
    CEDULA = 'CEDULA'
    ACTA_NACIMIENTO = 'ACTA_NACIMIENTO'
    RECORD_ESCUELA = 'RECORD_ESCUELA'

class EstadoDocumento:
    PENDIENTE = 'PENDIENTE'
    VALIDO = 'VALIDO'
    RECHAZADO = 'RECHAZADO'

class SizeDocumento:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB por documento

class EstadoEstudianteMateria:
    RETIRADA = 'RETIRADA'
    APROBADA = 'APROBADA'
    REPROBADA = 'REPROBADA'


class Calificacion:
    MINIMO_APROBACION = 70


class UNICDAEndpoints:
    BASE_URL = "https://localhost:7192"
    GENERATE_TOKEN = "/api/Auth/GenerateExternalAPIToken"
    EVENTOS_PAGINATION = "/api/Evento/GetPagination"
    ESTUDIANTES = "/api/Estudiantes"
    LIBROS_PAGINATION = "/api/Libro/GetPagination"
    PDF_MULTIMEDIA = "/api/MultimediaPreview/PDF"



class UnicdaPaginacion:
    PAGE = 1
    PAGESIZE = 10