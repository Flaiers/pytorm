from typing import Any, Dict, Generic, Sequence, TypeVar, overload

from sqlalchemy.ext.asyncio import AsyncSession

from pytorm.repository import AbstractRepository

T = TypeVar('T')

class Repository(AbstractRepository, Generic[T]):

    def __init__(self, session: AsyncSession) -> None: ...
    def create(self, **attrs) -> T: ...
    def merge(self, instance: T, **attrs) -> T: ...
    def has_pk(self, instance: T) -> bool: ...
    def get_pk(self, instance: T) -> Dict[str, Any] | Any: ...
    async def count(self, *where, **attrs) -> int: ...
    async def update(self, *where, values: Dict[str, Any], **attrs) -> None: ...
    async def delete(self, *where, **attrs) -> None: ...
    async def find(self, *where, **attrs) -> Sequence[T]: ...
    async def find_one(self, *where, **attrs) -> T | None: ...
    async def find_one_or_fail(self, *where, **attrs) -> T: ...
    @overload
    async def remove(self, instance: T) -> None: ...
    @overload
    async def remove(self, instances: Sequence[T]) -> None: ...
    @overload
    async def pre_save(self, instance: T) -> T: ...
    @overload
    async def pre_save(self, instances: Sequence[T]) -> Sequence[T]: ...
    @overload
    async def save(self, instance: T) -> T: ...
    @overload
    async def save(self, instances: Sequence[T]) -> Sequence[T]: ...

def InjectRepository(model: T, session: AsyncSession) -> Repository[T]: ...
