import asyncio
import enum
import os
import typing as t

import gino
import pytest
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as PostgresEnum

DB_SCHEMA = os.getenv("SCHEMA")
DB = gino.Gino(schema=DB_SCHEMA)


class Enum1(enum.Enum):
    VAL1 = enum.auto()
    VAL2 = enum.auto()


class Enum2(enum.Enum):
    VAL3 = enum.auto()
    VAL4 = enum.auto()
    VAL5 = enum.auto()


@pytest.mark.asyncio
class TestGinoEnum:

    @pytest.fixture(scope="session")
    async def engine(self):
        async with DB.with_bind(os.getenv("DATABASE")) as engine:
            yield engine

    @pytest.fixture(scope="session")
    def db_model(self, gino_enum_type, engine) -> gino.Gino.Model:
        if gino_enum_type == "postgres":
            class Foo(DB.Model):
                __tablename__ = "foo"

                id = DB.Column(DB.Integer(), primary_key=True)

                # causes asyncpg.exceptions.UndefinedObjectError: type "test.enum1" does not exist
                enum_field1 = DB.Column(PostgresEnum(Enum1, inherit_schema=True), default=Enum1.VAL1, nullable=False)
                enum_field2 = DB.Column(PostgresEnum(Enum2, inherit_schema=True), default=Enum2.VAL3, nullable=False)

        elif gino_enum_type is None:
            class Foo(DB.Model):
                __tablename__ = "foo"

                id = DB.Column(DB.Integer(), primary_key=True)

                # no exception
                enum_field1 = DB.Column(DB.Enum(Enum1, inherit_schema=True), default=Enum1.VAL1, nullable=False)
                enum_field2 = DB.Column(DB.Enum(Enum2, inherit_schema=True), default=Enum2.VAL3, nullable=False)

        else:
            raise ValueError("unknown gino type", gino_enum_type)

        return Foo

    @pytest.fixture()
    async def clean_database(self, gino_enum_type, gino_create_enum_type_manually, engine, db_model):
        await DB.gino.drop_all()

        if DB_SCHEMA:
            await engine.status(f"""drop schema if exists \"{DB_SCHEMA}\" cascade""")
            await engine.status(f"""create schema if not exists \"{DB_SCHEMA}\"""")

        if gino_create_enum_type_manually:
            def quote_value(value: t.Union[Enum1, Enum2]) -> str:
                return f"'{value.name}'"

            async def create_enum(e: t.Union[t.Type[Enum1], t.Type[Enum2]]) -> None:
                if DB_SCHEMA:
                    enum_type = f"\"{DB_SCHEMA}\".{e.__name__.lower()}"
                else:
                    enum_type = f"{e.__name__.lower()}"

                await engine.status(f"""
                    create enum type {enum_type} ({",".join(quote_value(v) for v in e)})
                """)

            await create_enum(Enum1)
            await create_enum(Enum2)

        else:
            # hope that enum types will be added automatically with `create_all` .
            pass

        await DB.gino.create_all()

    async def test_enum_types_removal(self, engine, clean_database) -> None:
        await DB.gino.drop_all()
        assert (await self.__get_enum_info_from_database(engine)) == []

    async def test_enum_type_creation(self, engine, clean_database) -> None:
        assert (await self.__get_enum_info_from_database(engine)) == sorted(
            (DB_SCHEMA or "public", enum_type.__name__.lower(), val.name)
            for enum_type in (Enum1, Enum2)
            for val in enum_type
        )

    @pytest.mark.parametrize("n", (0, 1, 2))
    async def test_enum_type_filter(self, engine, clean_database, db_model, n) -> None:
        assert (await asyncio.gather(*(
            self.__get_bars(engine, db_model)
            for i in range(n)
        ))) == [[] for i in range(n)]

    async def __get_bars(self, engine: gino.GinoEngine, db_model: gino.Gino.Model) -> [object]:
        val1 = await engine.all(db_model.query.where(db_model.enum_field1 == Enum1.VAL1))
        val4 = await engine.all(
            sa.select([db_model.id]).select_from(db_model).where(db_model.enum_field2 == Enum2.VAL4))

        return [*val1, *val4]

    async def __get_enum_info_from_database(self, engine: gino.GinoEngine) -> t.Sequence[t.Tuple[str, str, str]]:
        return await engine.all("""
            select n.nspname as enum_schema, t.typname as enum_name, e.enumlabel as enum_value
            from pg_type t
            join pg_enum e on t.oid = e.enumtypid
            join pg_catalog.pg_namespace n ON n.oid = t.typnamespace
            order by enum_schema, enum_name, enum_value
        """)
