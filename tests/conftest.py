import asyncio
import typing as t

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--gino-enum-type", dest="gino_enum_type", action="store", default=None)
    parser.addoption("--gino-create-enum-type-manually", dest="gino_create_enum_type_manually", action="store_true",
                     default=False)


@pytest.fixture(scope="session")
def gino_enum_type(pytestconfig: Config) -> t.Optional[str]:
    return pytestconfig.getoption("gino_enum_type")


@pytest.fixture(scope="session")
def gino_create_enum_type_manually(pytestconfig: Config) -> bool:
    return pytestconfig.getoption("gino_create_enum_type_manually")
