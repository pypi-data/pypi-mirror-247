# Validata Table

[Validata Table](https://gitlab.com/validata-table/validata-table)  is python package used as a tabular data validation service.

It includes four subpackages, where you can find their respective documentations :
- [`validata_core`](src/validata_core/README.md)
- [`validata_ui`](src/validata_ui/README.md)
- [`validata_api`](src/validata_api/README.md)
- `tests` used for testing the project (in development environment or in continuous integration)

It offers also a command line tool `validata` used to validate tabular data. 
See [validata_core/README.md](src/validata_core/README.md) for more details.

# Using `validata-table` package

You can use locally this package `validata-table`, doing:
```commandline
pip install validata-table 
```
This allows you to use `validata` command line tool to validate tabular data:
```commandline
validata --help
```

# Development

This project is based on [Docker](https://docs.docker.com/get-started/overview/) to use a local environement developement.

This project includes a Makefile, which allows you to run predefined actions 
by running specific commands.

Dependency management tool used : [Poetry version 1.6.1](https://python-poetry.org/docs/)

### Requirements

First install [Docker Engine](https://docs.docker.com/engine/install/) and [docker-compose >= version 2](https://docs.docker.com/compose/install/) 
on your machine if not already done.

Then you may clone source code in your deployment directory:
```commandline
git clone https://gitlab.com/validata-table/validata-table.git
cd validata-table
```

### Run on development local environment

Configuration is done by editing environment variables in `.env`, 
(see `.env.example` file to set `.env` file)

Warning: Docker env files do not support using quotes around variable values!

Launch the development local environment, thanks to the makefile command:
```bash
# in validata-table/
make serve_dev
```
This launches two docker containers:
- validata-table-api-dev
- validata-table-ui-dev

### Validata Table API (using `validata-table-api-dev` docker container)
To access to the API of Validata Table click on http://localhost:5000/

[Try Validata Table API](src/validata_api/README.md)

### Validata Table UI (using `validata-table-ui-dev` docker container)
To access to the API of Validata Table click on http://localhost:5001/

### Validata Table command line tool (using `validata-table-api-dev` docker container)
To use validata command line tool in the docker development environment, run:
  ```
  docker exec -it validata-table-api-dev bash
  validata --help
  ```

### Test
To launch tests in the development environment, run:
  ```make test```

### Linting
Some code linting tools are configured for this project:
- [black](https://black.readthedocs.io/en/stable/): to format code, run `make black`
- [isort](https://pycqa.github.io/isort/): to format import, run `make isort`
- [flake8](https://flake8.pycqa.org/en/latest/): to enforce style coding, run `make flake8`
- [pyright](https://microsoft.github.io/pyright/#/): to check static types.
  `pyright` will be executed in local virtual environment with `poetry`:
  
  First you need to create a virtual environment .venv at the root of the project
and configure it:
  ```commandline
  # At /validata-table/ root 
  python3.9 -m venv .venv  # install virtual environement locally
  poetry config virtualenvs.in-project true
  poetry config --list # Check if correctly configured
  >>>
  ...
  virtualenvs.in-project = true
  ...
  
  poetry install  # install project dependencies
  ```
  Then execute locally `pyright` with `poetry`:
  ```commandline
  poetry run pyright .
  ```


# Continuous Integration

The continuous integration is configured in `.gitlab-ci.yml` file

## Release a new version

On master branch :
- Update version in [pyproject.toml](pyproject.toml) and [CHANGELOG.md](CHANGELOG.md) files
- Update version Docker images used in [docker-compose.yml](docker-compose.yml) file:
  - registry.gitlab.com/validata-table/validata-table/validata-table-api:vX.X.X
  - registry.gitlab.com/validata-table/validata-table/validata-table-ui:vX.X.X
- Commit changes using `Release` as commit message
- Create git tag (starting with "v" for the release) `git tag -a`
- Git push: `git push && git push --tags`
- Check that pypi package is created and container images for validata_ui and validata_api are well-built 
([validata-table pipelines](https://gitlab.com/validata-table/validata-table/-/pipelines))

Creating and pushing a new release will trigger the pipeline in order to automatically:
- publish a new version of `validata-table` package on [PyPI](https://pypi.org/)
- build a new tag of the Docker image `validata-table-ui`, based on the new version just created of the package `validata-table`, and publish it on the gitlab container 
registry [validata-table-ui](https://gitlab.com/validata-table/validata-table/container_registry/5871420), 
used to run user interface Validata
- build a new tag of the Docker image `validata-table-api`, based on the new version just created of the package `validata-table` and publish it on the gitlab container 
registry [validata-table-api](https://gitlab.com/validata-table/validata-table/container_registry/5871449), 
used to run the API of Validata

This pipeline runs when a new tag under the format 'vX.X.X' is pushed.


# Deploy to production
You can deploy this project on your own production server by using Docker.

Production environment is based on Docker images `validata-table-ui`and `validata-table-api`
hosted on gitlab container registries [validata-table-ui](https://gitlab.com/validata-table/validata-table/container_registry/5871420)
and [validata-table-api](https://gitlab.com/validata-table/validata-table/container_registry/5871449)

To deploy in production, you can follow these steps described below.

First you may clone source code in your deployment directory:
```commandline
git clone https://gitlab.com/validata-table/validata-table.git
cd validata-table
```
Configuration is done by editing environment variables in `.env`, 
(see `.env.example` file to set `.env` file).

Warning: Docker env files do not support using quotes around variable values !

Launch the docker production environment with makefile:
```commandline
make serve_prod
```
OR launch the docker production environment with `docker compose` command:
```commandline
docker compose -f docker-compose.yml up --build -d
```
Then: 
- To access to the API of Validata Table click on http://localhost:<PORT_NUMBER_API>/
  (replacing PORT_NUMBER_API with the value you choose)
- To access to the UI of Validata Table click on http://localhost:<PORT_NUMBER_UI>/ 
  (replacing PORT_NUMBER_UI with the value you choose)
- To access to the `validata` command lines tool:
  ```
  docker exec -it validata-table-api bash
  validata --help
  ```

# History
To keep track of the project's history, [Validata Table](https://gitlab.com/validata-table/validata-table) 
comes from the merge of four gitlab repositories :
- [Validata core](https://gitlab.com/validata-table/validata-core)
- [Validata UI](https://gitlab.com/validata-table/validata-ui)
- [Validata API](https://gitlab.com/validata-table/validata-api)
- [Validata Docker](https://gitlab.com/validata-table/validata-docker)
