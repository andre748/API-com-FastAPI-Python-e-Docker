from pydantic import Field, UUID4
from typing import Annotated
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description="Nome da centro de treinamento", examples=["CT king"], max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", examples=["Rua das Flores, 123"], max_length=100)]
    proprietario: Annotated[str, Field(description="Nome do proprietário do centro de treinamento", examples=["João da Silva"], max_length=50)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta")]
    

class CentroTreinamentoIn(CentroTreinamento):
    pass

class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description="ID do centro de treinamento")]
    