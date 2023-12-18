# FastAPI Request helper

## How to use

1. Set a variable

```python
# user_service.py
from fastapi import FastAPI
from fastapi_global_variable import GlobalVariable

app = FastAPI(title="Application")

GlobalVariable.set('app', app)
```

2. Use variable

```python
from fastapi_global_variable import GlobalVariable

print(GlobalVariable.get_or_fail('app'))
print(GlobalVariable.get('app'))
```

3. Decorators

FastAPI Request Helper provides lots of helpful decorators:

- Swagger docs decorators: @controller, @tag, @get, @post, @put, @delete, @patch
- Rate limit request: @rate_limit
- FastAPI response model: @response
- FastAPI guards: @guard, @gurads
- FastAPI response status: @status
- FastAPI API info details: @description, @summary, @name
- FastAPI API response status: @status_no_content, @status_ok, @status_created
- Hide API: @hidden_when(condition: boolean)

Fast API Helper also provides Pagination Query params helper: PaginationParams

```python
# Sample
from fastapi_request_helper import (
    controller,
    post,
    rate_limit,
    response,
    status_created,
    status_no_content,
    status_ok,
    tag,
)

@controller('authentications')
@tag('Authentication')
class AuthenticationController:
    def __init__(self, auth_service: AuthenticationService = Depends()):
        self.auth_service = auth_service

    @post('create-email-otp')
    @status_no_content()
    async def create_email_otp(self):
        pass
```

## How to test in testpypi

1. Setup file .pypirc
```bash
$ cd ~/
```
```bash
$ vim .pypirc
```
Copy to file .pypirc
```text
[pypi]
username=****
password=****

[testpypi]
username=__token__
password=*****

[distutils]

index-servers =
  pypi
  testpypi
  gitlab

[gitlab]
repository = https://gitlab.com/api/v4/projects/50838104/packages/pypi
username = gitlab+deploy-token-3497403
password = ****
```
3. Increase the version in `pyproject.toml`
4. Run command

```bash
$ ./build_and_test.sh
```
5. install package
```bash
$ pip install --no-cache-dir --upgrade -i https://test.pypi.org/simple/ fastapi-request-helper==x.y.z --no-dependencies
$ pip install -i https://test.pypi.org/simple/ fastapi-request-helper==x.y.z
```

## How to publish new version

1. Increase the version in `pyproject.toml`
2. Run command

```bash
$ ./build_and_publish.sh
```
