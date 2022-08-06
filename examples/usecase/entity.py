import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin(object):

    created_at = sa.Column(
        sa.DateTime,
        default=sa.func.now(),
        server_default=sa.FetchedValue(),
    )
    updated_at = sa.Column(
        sa.DateTime,
        onupdate=sa.func.now(),
        server_default=sa.FetchedValue(),
        server_onupdate=sa.FetchedValue(),
    )
    deleted_at = sa.Column(sa.DateTime, server_default=sa.FetchedValue())


@as_declarative()
class Base(object):

    __name__: str
    metadata: MetaData

    @classmethod
    @declared_attr
    def __tablename__(cls):  # noqa: N805
        return cls.__name__.lower()

    id = sa.Column(
        psql.UUID(as_uuid=True),
        server_default=sa.text('gen_random_uuid()'),
        primary_key=True,
        index=True,
    )


class Application(TimestampMixin, Base):

    __mapper_args__ = {
        'eager_defaults': True,
        'always_refresh': True,
    }
    __table_args__ = (
        sa.UniqueConstraint('phone'),
        sa.UniqueConstraint('email'),
    )

    phone = sa.Column(sa.String(255), index=True, nullable=False)
    email = sa.Column(sa.String(255), index=True, nullable=False)
    text = sa.Column(sa.Text, nullable=False)
