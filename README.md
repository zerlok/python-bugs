# celery + pytest

A simple test with celery task invocation is written [here](tests/test_task.py). It starts a redis docker container,
then setup celery application with appropriate backend. After that a `foo` task is invoked. It is described
by `test-pytest-call` target in the `Makefile`.

A similar approach is made in `test-normal-call` target in the `Makefile`. It starts redis container via docker compose,
then starts a celery worker, waits for it to be ready, then it starts a simple [python script](src/call.py) with same
task invocation as in pytest.

Expected result: both targets finishes without errors.

Actual result: `test-pytest-call` target finishes with error (look traceback below).

## usage

Use `Makefile` to install dependencies and start test highlighting the issue

```shell
make all
```

## actual result in pytest

pytest returns error (task timeout)

```
Waiting for container to be ready.
FAILED [100%]
tests/test_task.py:43 (test_foo_returns_expected_result[3-4-foo(3, 4) == [6, 10, 14]])
self = <celery.backends.redis.ResultConsumer object at 0x7ffb0ba1ef70>
result = <AsyncResult: 22da8dd1-6982-4be6-a535-cfc16a3d610a>, timeout = 15.0
on_interval = <promise@0x7ffb0ba25940>, on_message = None
kwargs = {'interval': 0.5, 'no_ack': True}, prev_on_m = None, _ = None

    def _wait_for_pending(self, result,
                          timeout=None, on_interval=None, on_message=None,
                          **kwargs):
        self.on_wait_for_pending(result, timeout=timeout, **kwargs)
        prev_on_m, self.on_message = self.on_message, on_message
        try:
>           for _ in self.drain_events_until(
                    result.on_ready, timeout=timeout,
                    on_interval=on_interval):

.venv/lib/python3.9/site-packages/celery/backends/asynchronous.py:287: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <celery.backends.asynchronous.Drainer object at 0x7ffb0b9c6730>
p = <promise@0x7ffb0ba258b0 --> <weakref at 0x7ffb0ba03cf0; to 'AsyncResult' at 0x7ffb0ba1eee0>>
timeout = 15.0, interval = 1, on_interval = <promise@0x7ffb0ba25940>
wait = <bound method ResultConsumer.drain_events of <celery.backends.redis.ResultConsumer object at 0x7ffb0ba1ef70>>

    def drain_events_until(self, p, timeout=None, interval=1, on_interval=None, wait=None):
        wait = wait or self.result_consumer.drain_events
        time_start = time.monotonic()
    
        while 1:
            # Total time spent may exceed a single call to wait()
            if timeout and time.monotonic() - time_start >= timeout:
>               raise socket.timeout()
E               socket.timeout

.venv/lib/python3.9/site-packages/celery/backends/asynchronous.py:52: timeout

During handling of the above exception, another exception occurred:

redis_dsn = 'redis://127.0.0.1:6379'
celery_app = <Celery celery.tests at 0x7ffb0c700a90>
celery_worker = <Worker: gen113276@zerlok-x-book (running)>, x = 3, y = 4
expected_result = 'foo(3, 4) == [6, 10, 14]'

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
>       assert call_foo(x, y) == expected_result

tests/test_task.py:59: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/mytasks/call.py:5: in call_foo
    return foo.delay(x, y).get(timeout=15.0)
.venv/lib/python3.9/site-packages/celery/result.py:224: in get
    return self.backend.wait_for_pending(
.venv/lib/python3.9/site-packages/celery/backends/asynchronous.py:221: in wait_for_pending
    for _ in self._wait_for_pending(result, **kwargs):
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <celery.backends.redis.ResultConsumer object at 0x7ffb0ba1ef70>
result = <AsyncResult: 22da8dd1-6982-4be6-a535-cfc16a3d610a>, timeout = 15.0
on_interval = <promise@0x7ffb0ba25940>, on_message = None
kwargs = {'interval': 0.5, 'no_ack': True}, prev_on_m = None, _ = None

    def _wait_for_pending(self, result,
                          timeout=None, on_interval=None, on_message=None,
                          **kwargs):
        self.on_wait_for_pending(result, timeout=timeout, **kwargs)
        prev_on_m, self.on_message = self.on_message, on_message
        try:
            for _ in self.drain_events_until(
                    result.on_ready, timeout=timeout,
                    on_interval=on_interval):
                yield
                sleep(0)
        except socket.timeout:
>           raise TimeoutError('The operation timed out.')
E           celery.exceptions.TimeoutError: The operation timed out.

.venv/lib/python3.9/site-packages/celery/backends/asynchronous.py:293: TimeoutError

```
