from typing import Generic, TypeVar, List

from pydantic import BaseModel

# --- Definir un tipo genérico para el contenido de 'data' ---
# T representa cualquier BaseModel que queramos poner dentro de 'data'
Model = TypeVar('Model', bound=BaseModel)


class ResponseData(BaseModel, Generic[Model]):
    data: Model | None

class ResponseList(BaseModel, Generic[Model]):
    data: List[Model]
