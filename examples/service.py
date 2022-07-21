from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from examples.dto import ApplicationCreate
from examples.entity import Application
from examples.mocks import get_session
from pytorm.repository import InjectRepository


class ApplicationService(object):

    def __init__(
        self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.repository = InjectRepository(Application, session)

    async def create(self, dto: ApplicationCreate) -> Application:
        application = self.repository.create(**dto.dict())
        return await self.repository.save(application)
