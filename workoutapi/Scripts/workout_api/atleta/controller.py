from datetime import datetime 
from fastapi import APIRouter, status
from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from uuid import uuid4, UUID
from fastapi import Body, APIRouter, status, Body, HTTPException
from sqlalchemy.future import select
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()

@router.post(
        "/",
        summary="Criar novo atleta",
        status_code=status.HTTP_201_CREATED,
        response_model= AtletaOut
        )
async def post(
    db_session: DataBaseDependency, 
    atleta_in: AtletaIn = Body(...)
    ):  
        categoria = (await db_session.execute(
                select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))
                ).scalars().first()
        
        if not categoria:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A categoria {atleta_in.categoria.nome} não encontrada.")


        centro_treinamento = (await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))
                ).scalars().first()
        
        if not centro_treinamento:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"O Centro de trienamento {atleta_in.centro_treinamento.nome} não foi encontrada.")

        
        try:
                atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(),**atleta_in.model_dump())
                atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria" ,"centro_treinamento"}))
                atleta_model.categoria_id = categoria.pk_id
                atleta_model.centro_treinamento_id = centro_treinamento.pk_id


                # breakpoint() 

                db_session.add(atleta_model)
                await db_session.commit()
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocorreu um erro ao incerir os dados no banco: {e}")
        
        return atleta_out

@router.get(
        "/",
        summary="Consultar todos os atletas",
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaOut],

        )
async def query(db_session: DataBaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()

    return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
        "/{id}",
        summary="Consultar atleta pelo ID",
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,

        )
async def query(id: UUID, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no ID: {id}")
    return atleta


@router.patch(
        "/{id}",
        summary="Editar atleta pelo ID",
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut,
        )
async def get(id: UUID, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no ID: {id}")
    
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

        
    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaOut.model_validate(atleta)


@router.delete(
        "/{id}",
        summary="Deletar atleta pelo ID",
        status_code=status.HTTP_204_NO_CONTENT,
        )
async def get(id: UUID, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no ID: {id}")
    
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

        
    await db_session.delete(atleta)
    await db_session.commit()

    


