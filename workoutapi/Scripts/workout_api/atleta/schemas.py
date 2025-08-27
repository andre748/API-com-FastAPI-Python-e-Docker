from pydantic import BaseModel, Field, PositiveFloat
from typing import Annotated, Optional
from workout_api.contrib.schemas import BaseSchema
from workout_api.contrib.schemas import OutMixin
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", examples=["João Silva"], max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", examples=["12345678900"], max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", examples=[25])]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", examples=[70.5])]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", examples=[1.75])]
    sexo: Annotated[str, Field(description="Sexo do atleta", examples=['M'], max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do atleta")] 
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]   

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    #id: int = Field(description="ID do atleta", example=1)
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do atleta",  examples=["João Silva"],max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", examples=[25])]
    peso: Annotated[Optional[PositiveFloat], Field(None, description="Peso do atleta em kg", examples=[70.5])]
