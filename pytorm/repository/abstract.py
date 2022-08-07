from abc import ABC, abstractmethod
from typing import Any, Dict, List, Sequence, Type, TypeVar

from multimethod import multimethod as overload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

Model = TypeVar('Model')


class AbstractRepository(ABC):

    session: AsyncSession
    model_cls: Type[Model]
    query_cls: Type[Query]

    @abstractmethod
    def query(self, *entities) -> Query:
        raise NotImplementedError

    @abstractmethod
    def create(self, **attrs) -> Model:
        raise NotImplementedError

    @abstractmethod
    def merge(self, instance: Model, **attrs) -> Model:
        raise NotImplementedError

    @abstractmethod
    def has_pk(self, instance: Model) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_pk(self, instance: Model) -> Dict[str, Any] | Any:
        raise NotImplementedError

    @abstractmethod
    async def count(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        *where,
        values: Dict[str, Any],
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> List[Model]:
        raise NotImplementedError

    @abstractmethod
    async def find_one(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> Model | None:
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_fail(self, *where, **attrs) -> Model:
        raise NotImplementedError

    @abstractmethod
    @overload
    async def remove(self, instance: Model) -> None:
        raise NotImplementedError

    @abstractmethod
    @overload
    async def remove(self, instances: Sequence[Model]) -> None:
        raise NotImplementedError

    @abstractmethod
    @overload
    async def pre_save(self, instance: Model, **kwargs) -> Model:
        raise NotImplementedError

    @abstractmethod
    @overload
    async def pre_save(self, instances: Sequence[Model]) -> Sequence[Model]:
        raise NotImplementedError

    @abstractmethod
    @overload
    async def save(self, instance: Model, **kwargs) -> Model:
        raise NotImplementedError

    @abstractmethod
    @overload
    async def save(self, instances: Sequence[Model]) -> Sequence[Model]:
        raise NotImplementedError
