import os

from celery import Celery, group
# noinspection PyProtectedMember
from celery.result import allow_join_result

BROKER_URL = os.getenv("MYTASKS_BROKER_URL", "redis://localhost:6379")
app = Celery(
    name='tasks',
    broker_url=BROKER_URL,
    result_backend=BROKER_URL,
)


@app.task
def foo(x, y):
    pipeline = group([bar.si(i, y) for i in range(x)]) | baz.s("foo", (x, y))

    # result of `foo` may be used in other tasks, so wait for subtasks result
    with allow_join_result():
        return pipeline.delay().get()


@app.task
def bar(z, y):
    return sum(z + i for i in range(y))


@app.task
def baz(res, fname, args):
    return f"""{fname}({", ".join(str(a) for a in args)}) == {res}"""

# if __name__ == "__main__":
#     app.start(["-A", ""])
