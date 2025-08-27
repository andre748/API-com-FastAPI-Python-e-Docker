from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from workout_api.configs.database import get_session

DataBaseDependency = Annotated[AsyncSession, Depends(get_session)]