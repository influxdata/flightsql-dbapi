## Dev instructions

## Pre-requisites 
- Python version 3 or greater
- Clone superset: https://github.com/apache/superset

## Superset Directory
- Create a requirements-local.txt in the docker directory. This will specify version of the package you want to build.

E.g.

```
$ cat docker/requirements-local.txt
http://docker.for.mac.host.internal:8000/dist/flightsql_dbapi-0.2.0.tar.gz#egg=flightsql-dbapi
```

- Run superset using docker compose:

`docker-compose -f ./docker-compose-non-dev.yml up`

## Building the flightsql-dbapi

- run `make build`

- expose a http server: `python3 -m http.server 8000`

To verify that docker is communiciating on port 8000 you should see requests such as this in the logs: 

127.0.0.1 - - [15/Feb/2023 12:43:25] "GET /dist/flightsql_dbapi-0.2.1.tar.gz HTTP/1.1" 200 -

## Testing it on Superset:

- Select other as the type and name appropriately

- Provide a URI: 

`datafusion+flightsql://${host}:${port}/?bucket-name=${my-bucket}&token=${my-token}`

- Create a chart - select add dataset and select your named database and schema.

## Dependency Management

- Handle dependencies using direnv and a .envrc, this sets your venv as a pre-requisite to all other make targets.

- `brew install direnv`

- create a .envrc, setting the venv and layout to python:

```
$ cat .envrc
export VIRTUAL_ENV=venv
layout python3
 ```

- If using zsh add the following to your .zshrc:

`eval "$(direnv hook zsh)"`

If you make changes to your .envrc it should ask you to accept the changes ie:

`direnv allow .`
