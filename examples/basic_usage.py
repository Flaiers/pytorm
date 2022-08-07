import asyncio
from typing import List
from uuid import UUID

from examples.service import ApplicationService
from examples.usecase.database import context_session
from examples.usecase.dto import (
    ApplicationCreate,
    ApplicationFilter,
    ApplicationRead,
)


async def read_applications(
    application_service: ApplicationService,
) -> List[ApplicationRead]:
    dto = ApplicationFilter()
    applications = await application_service.find(dto)
    return [
        ApplicationRead.from_orm(application)
        for application in applications
    ]


async def read_application(
    application_service: ApplicationService, application_id: UUID,
) -> ApplicationRead:
    application = await application_service.find_one_or_fail(application_id)
    return ApplicationRead.from_orm(application)


async def create_application(
    application_service: ApplicationService,
) -> ApplicationRead:
    dto = ApplicationCreate()
    application = await application_service.create(dto)
    return ApplicationRead.from_orm(application)


async def delete_application(
    application_service: ApplicationService, application_id: UUID,
) -> ApplicationRead:
    application = await application_service.delete(application_id)
    return ApplicationRead.from_orm(application)


async def main() -> None:
    async with context_session() as session:
        application_service = ApplicationService(session)
        await read_applications(application_service)
        application = await create_application(application_service)
        await read_application(application_service, application.id)
        await delete_application(application_service, application.id)


if __name__ == '__main__':
    asyncio.run(main())
