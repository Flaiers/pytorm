import uuid
from typing import Sequence

import sqlalchemy as sa
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from examples.usecase.dto import ApplicationCreate, ApplicationFilter
from examples.usecase.entity import Application
from examples.usecase.mocks import get_session
from pytorm.repository import InjectRepository


class ApplicationService(object):

    def __init__(
        self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.repository = InjectRepository(Application, session)

    async def create(self, dto: ApplicationCreate) -> Application:
        application = self.repository.create(**dto.dict())
        return await self.repository.save(application)

    async def find(self, dto: ApplicationFilter) -> Sequence[Application]:
        return await self.repository.find(
            Application.deleted_at.is_(None),
            Application.phone.contains(dto.phone),
            Application.email.contains(dto.email),
        )

    async def find_one_or_fail(self, application_id: uuid.UUID) -> Application:
        return await self.repository.find_one_or_fail(
            Application.deleted_at.is_(None), id=application_id,
        )

    async def delete(self, application_id: uuid.UUID) -> Application:
        application = await self.find_one_or_fail(application_id)
        self.repository.merge(application, deleted_at=sa.func.now())
        return await self.repository.save(application)
