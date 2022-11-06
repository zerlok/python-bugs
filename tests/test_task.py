"""This module provides a failing test, which should work

Module was written according to example from the docs: https://docs.celeryq.dev/en/stable/userguide/testing.html#celery-worker-embed-live-worker

Found related issues:
 - https://github.com/celery/celery/issues/3642
 - https://github.com/celery/celery/issues/4039
"""

import pytest
from pytest_docker_tools import container as docker_container
from pytest_docker_tools.wrappers import Container

from mytasks.call import call_foo

pytestmark = [
    pytest.mark.celery,
]

_REDIS_PORT = "6379/tcp"
redis = docker_container(
    image="redis:7.0.4-alpine3.16",
    scope="session",
    ports={
        _REDIS_PORT: _REDIS_PORT,
    },
)


@pytest.fixture(scope="session")
def redis_dsn(redis: Container):
    assert redis.ready()
    host, port = redis.get_addr(_REDIS_PORT)

    yield f"""redis://{host}:{port}"""

    assert redis.ready()


@pytest.fixture()
def celery_config(redis_dsn):
    return {"broker_url": redis_dsn, "result_backend": redis_dsn}


@pytest.mark.parametrize("x,y,expected_result", [
    pytest.param(3, 4, "foo(3, 4) == [6, 10, 14]"),
])
def test_foo_returns_expected_result(
        redis_dsn,
        celery_app,
        celery_worker,
        x,
        y,
        expected_result,
) -> None:
    assert celery_app.backend.url == redis_dsn
    # FIXME: task call fails with timeout, but should be passed without any failure
    #  >           raise TimeoutError('The operation timed out.')
    #  E           celery.exceptions.TimeoutError: The operation timed out.
    assert call_foo(x, y) == expected_result
