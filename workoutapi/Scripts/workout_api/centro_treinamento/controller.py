
from fastapi import APIRouter, status, Body, HTTPException
from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from uuid import UUID, uuid4
from sqlalchemy.future import select


router = APIRouter()

@router.post(
        path="/",
        summary="Criar novo centro de treinamento",
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut,

        )
async def post(
    db_session: DataBaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
    ) -> CentroTreinamentoOut:

    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.commit()
    
    return centro_treinamento_out

@router.get(
        "/",
        summary="Consultar todas os centros de treinamento",
        status_code=status.HTTP_200_OK,
        response_model=list[CentroTreinamentoOut],

        )
async def query(db_session: DataBaseDependency) -> list[CentroTreinamentoOut]:
    centro_treinamentos: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return centro_treinamentos

@router.get(
        "/{id}",
        summary="Consultar uma centro_treinamento pelo ID",
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut,

        )
async def query(id: UUID, db_session: DataBaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()

    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"centro de treinamento não encontrada no ID: {id}")
    return centro_treinamento