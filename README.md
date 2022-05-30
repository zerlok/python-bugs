# python-bugs

use this project to quickly reproduce my bugs with python related tasks

## sqlalchemy, postgres, Enum

* python dependencies
  ```
  asyncpg==0.25.0; python_full_version >= "3.6.0"
  atomicwrites==1.4.0; python_version >= "3.7" and python_full_version < "3.0.0" and sys_platform == "win32" or sys_platform == "win32" and python_version >= "3.7" and python_full_version >= "3.4.0"
  attrs==21.4.0; python_version >= "3.7" and python_full_version < "3.0.0" or python_full_version >= "3.5.0" and python_version >= "3.7"
  click==8.1.3; python_version >= "3.7"
  colorama==0.4.4; python_version >= "3.7" and python_full_version < "3.0.0" and sys_platform == "win32" and platform_system == "Windows" or sys_platform == "win32" and python_version >= "3.7" and python_full_version >= "3.5.0" and platform_system == "Windows"
  greenlet==1.1.2; python_version >= "3" and python_full_version < "3.0.0" and (platform_machine == "aarch64" or platform_machine == "ppc64le" or platform_machine == "x86_64" or platform_machine == "amd64" or platform_machine == "AMD64" or platform_machine == "win32" or platform_machine == "WIN32") and (python_version >= "2.7" and python_full_version < "3.0.0" or python_full_version >= "3.6.0") or python_version >= "3" and (platform_machine == "aarch64" or platform_machine == "ppc64le" or platform_machine == "x86_64" or platform_machine == "amd64" or platform_machine == "AMD64" or platform_machine == "win32" or platform_machine == "WIN32") and (python_version >= "2.7" and python_full_version < "3.0.0" or python_full_version >= "3.6.0") and python_full_version >= "3.5.0"
  iniconfig==1.1.1; python_version >= "3.7"
  packaging==21.3; python_version >= "3.7"
  pluggy==1.0.0; python_version >= "3.7"
  py==1.11.0; python_version >= "3.7" and python_full_version < "3.0.0" or python_full_version >= "3.5.0" and python_version >= "3.7"
  pyparsing==3.0.9; python_full_version >= "3.6.8" and python_version >= "3.7"
  pytest-asyncio==0.18.3; python_version >= "3.7"
  pytest==7.1.2; python_version >= "3.7"
  sqlalchemy==1.4.36; (python_version >= "2.7" and python_full_version < "3.0.0") or (python_full_version >= "3.6.0")
  tomli==2.0.1; python_version >= "3.7"
  wait-for-it==2.2.1; python_version >= "3.7"
  ```

* postgres
    ```
    Container                Repository          Tag                 Image Id            Size
    python-bugs-postgres-1   postgres            11.10               13b1e1a60806        282MB
    ```

## sqlalchemy async

### run

```
docker-compose run --rm test-sqlalchemy-enum
```

### warnings

no

### errors

no

### expected

test pass without errors
