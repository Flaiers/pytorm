from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, List, Sequence, Type, TypeVar, overload

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Query

Base: DeclarativeMeta = declarative_base()
Model = TypeVar('Model', bound=Base)


class AbstractRepository(ABC):

    session: ClassVar[AsyncSession]
    model_cls: ClassVar[Type[Model]]
    query_cls: ClassVar[Type[Query]]

    @classmethod
    @abstractmethod
    def query(cls, *entities) -> Query:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, **attrs) -> Model:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def merge(cls, instance: Model, **attrs) -> Model:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def has_pk(cls, instance: Model) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_pk(cls, instance: Model) -> Dict[str, Any] | Any:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def count(
        cls,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update(
        cls,
        *where,
        values: Dict[str, Any],
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def delete(
        cls,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def find(
        cls,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> List[Model]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def find_one(
        cls,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> Model | None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def find_one_or_fail(cls, *where, **attrs) -> Model:
        raise NotImplementedError

    @overload
    @classmethod
    @abstractmethod
    async def remove(cls, instance: Model) -> None:
        raise NotImplementedError

    @overload
    @classmethod
    @abstractmethod
    async def remove(cls, instances: Sequence[Model]) -> None:
        raise NotImplementedError

    @overload
    @classmethod
    @abstractmethod
    async def pre_save(cls, instance: Model, **kwargs) -> Model:
        raise NotImplementedError

    @overload
    @classmethod
    @abstractmethod
    async def pre_save(cls, instances: Sequence[Model]) -> Sequence[Model]:
        raise NotImplementedError

    @overload
    @classmethod
    @abstractmethod
    async def save(cls, instance: Model, **kwargs) -> Model:
        raise NotImplementedError

    @overload
    @classmethod
    @abstractmethod
    async def save(cls, instances: Sequence[Model]) -> Sequence[Model]:
        raise NotImplementedError
