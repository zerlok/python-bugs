from mytasks.tasks import BROKER_URL, foo


def call_foo(x, y):
    return foo.delay(x, y).get(timeout=15.0)


if __name__ == "__main__":
    print(BROKER_URL)
    result = call_foo(3, 4)
    print(result)
    assert result == "foo(3, 4) == [6, 10, 14]"
