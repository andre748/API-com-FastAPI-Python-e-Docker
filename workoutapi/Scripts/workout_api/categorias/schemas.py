from pydantic import Field, UUID4
from typing import Annotated
from workout_api.contrib.schemas import BaseSchema


class Categoria(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", examples=["Scale"], max_length=10)]

class CategoriaIn(Categoria):
    pass

class CategoriaOut(Categoria):
    id: Annotated[UUID4, Field(description="ID da categoria")]