from typing import Any, Dict, Generic, List, Sequence, Type, TypeVar

import sqlalchemy as sa
from multimethod import multimethod as overload
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from pytorm.repository import AbstractRepository

Model = TypeVar('Model')


class Repository(AbstractRepository, Generic[Model]):

    def query(self, *entities) -> Query:
        return self.query_cls(entities, self.session)

    def create(self, **attrs) -> Model:
        return self.model_cls(**attrs)

    def merge(self, instance: Model, **attrs) -> Model:
        for attr_key, attr_value in attrs.items():
            setattr(instance, attr_key, attr_value)

        return instance

    def has_pk(self, instance: Model) -> bool:
        return bool(self.get_pk(instance))

    def get_pk(self, instance: Model) -> Dict[str, Any] | Any:
        server_default_pks = (
            pk
            for pk in self.model_cls.__mapper__.primary_key
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

    async def count(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> int:
        statement = sa.select(sa.func.count(
        )).select_from(self.model_cls).where(*where).filter_by(**attrs)
        return await self.session.scalar(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )

    async def update(
        self,
        *where,
        values: Dict[str, Any],
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> None:
        statement = sa.update(
            self.model_cls,
        ).where(*where).filter_by(**attrs).values(**values)
        await self.session.execute(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )
        await self.session.commit()

    async def delete(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> None:
        statement = sa.delete(self.model_cls).where(*where).filter_by(**attrs)
        await self.session.execute(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )
        await self.session.commit()

    async def find(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> List[Model]:
        statement = sa.select(self.model_cls).where(*where).filter_by(**attrs)
        return (await self.session.scalars(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )).unique().all()

    async def find_one(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> Model | None:
        statement = sa.select(self.model_cls).where(*where).filter_by(**attrs)
        return await self.session.scalar(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )

    async def find_one_or_fail(self, *where, **attrs) -> Model:
        instance = await self.find_one(*where, **attrs)
        if instance is None:
            raise NoResultFound('{0.__name__} not found'.format(self.model_cls))

        return instance

    @overload
    async def remove(self, instance: Model) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    @overload
    async def remove(self, instances: Sequence[Model]) -> None:
        for instance in instances:
            await self.session.delete(instance)

        await self.session.commit()

    @overload
    async def pre_save(self, instance: Model, **kwargs) -> Model:
        if self.has_pk(instance):
            return await self.session.merge(instance, **kwargs)

        self.session.add(instance, **kwargs)
        await self.session.flush([instance])
        return instance

    @overload
    async def pre_save(self, instances: Sequence[Model]) -> Sequence[Model]:
        self.session.add_all(instances)
        await self.session.flush(instances)
        return instances

    @overload
    async def save(self, instance: Model, **kwargs) -> Model:
        instance = await self.pre_save(instance, **kwargs)
        await self.session.commit()
        return instance

    @overload
    async def save(self, instances: Sequence[Model]) -> Sequence[Model]:
        instances = await self.pre_save(instances)
        await self.session.commit()
        return instances


def InjectRepository(
    model_cls: Type[Model],
    session: AsyncSession,
    query_cls: Type[Query] = Query,
) -> Repository[Model]:
    class_name = '{0.__name__}{1.__name__}'.format(model_cls, Repository)
    class_bases = (Repository,)
    class_namespace = {
        'session': session,
        'model_cls': model_cls,
        'query_cls': query_cls,
    }
    return type(class_name, class_bases, class_namespace)()
