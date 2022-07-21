from typing import Any, Dict, Sequence, Type, TypeVar, overload

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()
Model = TypeVar('Model', bound=Base)


class AbstractRepository(object):

    model: Type[Model]

    def create(self, **attrs) -> Model:
        raise NotImplementedError

    def merge(self, instance: Model, **attrs) -> Model:
        raise NotImplementedError

    def has_pk(self, instance: Model) -> bool:
        raise NotImplementedError

    def get_pk(self, instance: Model) -> Dict[str, Any] | Any:
        raise NotImplementedError

    async def count(self, *where, **attrs) -> int:
        raise NotImplementedError

    async def update(self, *where, values: Dict[str, Any], **attrs) -> None:
        raise NotImplementedError

    async def delete(self, *where, **attrs) -> None:
        raise NotImplementedError

    async def find(self, *where, **attrs) -> Sequence[Model]:
        raise NotImplementedError

    async def find_one(self, *where, **attrs) -> Model | None:
        raise NotImplementedError

    async def find_one_or_fail(self, *where, **attrs) -> Model:
        raise NotImplementedError

    @overload
    async def remove(self, instance: Model) -> None:
        raise NotImplementedError

    @overload
    async def remove(self, instances: Sequence[Model]) -> None:
        raise NotImplementedError

    @overload
    async def pre_save(self, instance: Model) -> Model:
        raise NotImplementedError

    @overload
    async def pre_save(self, instances: Sequence[Model]) -> Sequence[Model]:
        raise NotImplementedError

    @overload
    async def save(self, instance: Model) -> Model:
        raise NotImplementedError

    @overload
    async def save(self, instances: Sequence[Model]) -> Sequence[Model]:
        raise NotImplementedError
