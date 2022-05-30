# python-bugs

use this project to quickly reproduce my bugs with python related tasks

## Troubles with GINO, sqlalchemy, postgres, Enum

* python dependencies
    ```
    asyncpg==0.25.0; python_version >= "3.5" and python_version < "4.0" and python_full_version >= "3.6.0"
    atomicwrites==1.4.0; python_version >= "3.7" and python_full_version < "3.0.0" and sys_platform == "win32" or sys_platform == "win32" and python_version >= "3.7" and python_full_version >= "3.4.0"
    attrs==21.4.0; python_version >= "3.7" and python_full_version < "3.0.0" or python_full_version >= "3.5.0" and python_version >= "3.7"
    click==8.1.3; python_version >= "3.7"
    colorama==0.4.4; python_version >= "3.7" and python_full_version < "3.0.0" and sys_platform == "win32" and platform_system == "Windows" or sys_platform == "win32" and python_version >= "3.7" and python_full_version >= "3.5.0" and platform_system == "Windows"
    gino==1.0.1; python_version >= "3.5" and python_version < "4.0"
    iniconfig==1.1.1; python_version >= "3.7"
    packaging==21.3; python_version >= "3.7"
    pluggy==1.0.0; python_version >= "3.7"
    py==1.11.0; python_version >= "3.7" and python_full_version < "3.0.0" or python_full_version >= "3.5.0" and python_version >= "3.7"
    pyparsing==3.0.9; python_full_version >= "3.6.8" and python_version >= "3.7"
    pytest-asyncio==0.18.3; python_version >= "3.7"
    pytest==7.1.2; python_version >= "3.7"
    sqlalchemy==1.3.24; python_version >= "3.5" and python_full_version < "3.0.0" and python_version < "4.0" or python_version >= "3.5" and python_version < "4.0" and python_full_version >= "3.4.0"
    tomli==2.0.1; python_version >= "3.7"
    wait-for-it==2.2.1; python_version >= "3.7"
    ```

* postgres
    ```
    Container                Repository          Tag                 Image Id            Size
    python-bugs-postgres-1   postgres            11.10               13b1e1a60806        282MB
    ```

## db.Enum

### run

```
docker-compose run --rm test-simple-enum
```

### warnings

no

### errors

```
FAILED tests/test_gino.py::TestGinoEnum::test_enum_type_filter[2] - asyncpg.exceptions.InternalServerError: cache lookup failed for type 16453
```

### expected

test pass without errors

## postgresql.ENUM

### run

```
docker-compose run --rm test-postgres-enum
```

### warnings

```
tests/test_gino.py::TestGinoEnum::test_enum_types_removal
tests/test_gino.py::TestGinoEnum::test_enum_type_creation
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[0]
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[1]
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[2]
  /root/.cache/pypoetry/virtualenvs/python-bug-reports-VsnhxLU2-py3.9/lib/python3.9/site-packages/sqlalchemy/dialects/postgresql/base.py:1577: RuntimeWarning: coroutine 'GinoConnection._run_visitor' was never awaited
    bind._run_visitor(self.EnumDropper, self, checkfirst=checkfirst)
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

tests/test_gino.py::TestGinoEnum::test_enum_types_removal
tests/test_gino.py::TestGinoEnum::test_enum_type_creation
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[0]
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[1]
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[2]
  /root/.cache/pypoetry/virtualenvs/python-bug-reports-VsnhxLU2-py3.9/lib/python3.9/site-packages/sqlalchemy/dialects/postgresql/base.py:1557: RuntimeWarning: coroutine 'GinoConnection._run_visitor' was never awaited
    bind._run_visitor(self.EnumGenerator, self, checkfirst=checkfirst)
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
```

### errors

```
ERROR tests/test_gino.py::TestGinoEnum::test_enum_types_removal - asyncpg.exceptions.UndefinedObjectError: type "test-schema.enum1" does not exist
ERROR tests/test_gino.py::TestGinoEnum::test_enum_type_creation - asyncpg.exceptions.UndefinedObjectError: type "test-schema.enum1" does not exist
ERROR tests/test_gino.py::TestGinoEnum::test_enum_type_filter[0] - asyncpg.exceptions.UndefinedObjectError: type "test-schema.enum1" does not exist
ERROR tests/test_gino.py::TestGinoEnum::test_enum_type_filter[1] - asyncpg.exceptions.UndefinedObjectError: type "test-schema.enum1" does not exist
ERROR tests/test_gino.py::TestGinoEnum::test_enum_type_filter[2] - asyncpg.exceptions.UndefinedObjectError: type "test-schema.enum1" does not exist
```

### expected

test pass without errors

## postgresql.ENUM + manual enum creation

### run

```
docker-compose run --rm test-postgres-enum-manual
```

### warnings

```
tests/test_gino.py::TestGinoEnum::test_enum_types_removal
tests/test_gino.py::TestGinoEnum::test_enum_type_creation
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[0]
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[1]
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[2]
  /root/.cache/pypoetry/virtualenvs/python-bug-reports-VsnhxLU2-py3.9/lib/python3.9/site-packages/sqlalchemy/dialects/postgresql/base.py:1577: RuntimeWarning: coroutine 'GinoConnection._run_visitor' was never awaited
    bind._run_visitor(self.EnumDropper, self, checkfirst=checkfirst)
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

tests/test_gino.py::TestGinoEnum::test_enum_types_removal
tests/test_gino.py::TestGinoEnum::test_enum_type_creation
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[0]
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[1]
tests/test_gino.py::TestGinoEnum::test_enum_type_filter[2]
  /root/.cache/pypoetry/virtualenvs/python-bug-reports-VsnhxLU2-py3.9/lib/python3.9/site-packages/sqlalchemy/dialects/postgresql/base.py:1557: RuntimeWarning: coroutine 'GinoConnection._run_visitor' was never awaited
    bind._run_visitor(self.EnumGenerator, self, checkfirst=checkfirst)
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resource-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
```

### errors

```
FAILED tests/test_gino.py::TestGinoEnum::test_enum_types_removal - AssertionError: assert [('test-schem...um2', 'VAL5')] == []
FAILED tests/test_gino.py::TestGinoEnum::test_enum_type_filter[2] - asyncpg.exceptions.InternalServerError: cache lookup failed for type 16453
```

### expected

test pass without errors
