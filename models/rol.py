# models/rol.py
from enum import Enum

class Rol(str, Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    USUARIO = "USUARIO"