# Test Game

API for parsing and transforming arrays

## Getting Started

To have a copy of the repository on your machine we must clone the repository

* Clone repository
```ssh
    git clone git@github.com:pollitosabroson/game.git
```

### Prerequisites

Make sure that you have met the following prerequisites before continuing with this tutorial.

* Logged in as a user with sudo privileges or Admin user for MAC.
* Have [Docker](https://docs.docker.com/install/) installed

### Installing

To install the project, we must access the docker folder, after the environment we are going to execute, in this case it is the one of dev and we execute the following commands.

* access folder
```ssh
  cd game/docker/dev
```
* Create dockers
```ssh
  docker-compose build --no-cache --force-rm
```
* Run dockers
```ssh
  docker-compose up -d
```
* Apply migrations
```ssh
  docker exec -it api_dev_tangelo_api_1 python manage.py migrate
```

* Access

    * API: [localhost:8091](http://localhost:8091/)

### Endpoints

- Assignment
    - List all values
        -  http://localhost:8091/api/v1/
    - List of envs
        http://localhost:8091/api/v1/envs
    -  List parse vale from a list
        -  http://localhost:8091/api/v1/parse-from-list
    -  List parse vale from a string
        -  http://localhost:8091/api/v1/parse-from-str

## Running the tests

To run the tests just execute them via docker exec
* API
```ssh
  docker exec -it api_dev_tangelo_api_1 pytest -v
```

## Project scaffolding

- api
    - Core
        - Application that manages functions that are used in multiple applications
    - Assignment
        - Application to manage all parse values
- Docker
    - Dev
        - All configs for development
