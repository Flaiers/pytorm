from typing import Any, Dict, Generic, Sequence, Type, TypeVar

import sqlalchemy as sa
from multimethod import multimethod as overload
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Query

from pytorm.repository import AbstractRepository

Base: DeclarativeMeta = declarative_base()
Model = TypeVar('Model', bound=Base)


class Repository(AbstractRepository, Generic[Model]):

    @classmethod
    def query(cls, *entities) -> Query:
        return cls.query_cls(entities, cls.session)

    @classmethod
    def create(cls, **attrs) -> Model:
        return cls.model_cls(**attrs)

    @classmethod
    def merge(cls, instance: Model, **attrs) -> Model:
        for attr_key, attr_value in attrs.items():
            setattr(instance, attr_key, attr_value)

        return instance

    @classmethod
    def has_pk(cls, instance: Model) -> bool:
        return bool(cls.get_pk(instance))

    @classmethod
    def get_pk(cls, instance: Model) -> Dict[str, Any] | Any:
        server_default_pks = (
            pk
            for pk in cls.model_cls.__mapper__.primary_key
            if pk.server_default is not None
        )
        pks = {
            pk.name: attr
            for pk in server_default_pks
            if (attr := getattr(instance, pk.name)) is not None
        }

        if len(pks) > 1:
            return pks

        return next(iter(pks.values()))

    @classmethod
    async def count(cls, *where, **attrs) -> int:
        statement = sa.select(sa.func.count(
        )).select_from(cls.model_cls).where(*where).filter_by(**attrs)
        return await cls.session.scalar(statement)

    @classmethod
    async def update(cls, *where, values: Dict[str, Any], **attrs) -> None:
        statement = sa.update(cls.model_cls).where(*where).filter_by(**attrs).values(**values)
        await cls.session.execute(statement)
        await cls.session.commit()

    @classmethod
    async def delete(cls, *where, **attrs) -> None:
        statement = sa.delete(cls.model_cls).where(*where).filter_by(**attrs)
        await cls.session.execute(statement)
        await cls.session.commit()

    @classmethod
    async def find(cls, *where, **attrs) -> Sequence[Model]:
        statement = sa.select(cls.model_cls).where(*where).filter_by(**attrs)
        return (await cls.session.scalars(statement)).unique().all()

    @classmethod
    async def find_one(cls, *where, **attrs) -> Model | None:
        statement = sa.select(cls.model_cls).where(*where).filter_by(**attrs)
        return await cls.session.scalar(statement)

    @classmethod
    async def find_one_or_fail(cls, *where, **attrs) -> Model:
        instance = await cls.find_one(*where, **attrs)
        if instance is None:
            raise NoResultFound('{0.__name__} not found'.format(cls.model_cls))

        return instance

    @overload
    @classmethod
    async def remove(cls, instance: Model) -> None:
        await cls.session.delete(instance)
        await cls.session.commit()

    @overload
    @classmethod
    async def remove(cls, instances: Sequence[Model]) -> None:
        for instance in instances:
            await cls.session.delete(instance)

        await cls.session.commit()

    @overload
    @classmethod
    async def pre_save(cls, instance: Model) -> Model:
        if cls.has_pk(instance):
            return await cls.session.merge(instance)

        cls.session.add(instance)
        await cls.session.flush()
        return instance

    @overload
    @classmethod
    async def pre_save(cls, instances: Sequence[Model]) -> Sequence[Model]:
        cls.session.add_all(instances)
        await cls.session.flush()
        return instances

    @overload
    @classmethod
    async def save(cls, instance: Model) -> Model:
        instance = await cls.pre_save(instance)
        await cls.session.commit()
        return instance

    @overload
    @classmethod
    async def save(cls, instances: Sequence[Model]) -> Sequence[Model]:
        instances = await cls.pre_save(instances)
        await cls.session.commit()
        return instances


def InjectRepository(
    model_cls: Type[Model], session: AsyncSession, query_cls: Type[Query] = Query,
) -> Type[Repository[Model]]:
    class_name = '{0.__name__}{1.__name__}'.format(model_cls, Repository)
    class_bases = (Repository,)
    class_namespace = {'session': session, 'model_cls': model_cls, 'query_cls': query_cls}
    return type(class_name, class_bases, class_namespace)
