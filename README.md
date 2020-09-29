# Esports Challenge

![Run application tests](https://github.com/aless10/EsportsApp/workflows/Run%20application%20tests/badge.svg)

## TOC

* [Version](#version)
* [Description](#description)
* [How to run](#how-to-run)
* [Miscellanea](#miscellanea)

## Version

0.0.1.dev

## Description

#### Intro
JSON formatted messages are being published into a RabbitMQ queue (can be done manually on the RabbitMQ management UI).
Each one of the messages represents detailed information for an eSports event and has a source referenced. Your task is to read them, save them (update if necessary) and provide the information for further use.

Do not change the content of the message JSONs, since their content is intended to be as they are and they must be consumed in order.

#### Features
* Run RabbitMQ in a docker container (with a docker-compose configuration)
* Publish and consume messages with the Python package 'pika'
* Consumed messages are stored in a database in models like:
    
    * Title
    * Tournament
    * Team
    * Match
    * Scores of a Team in a Match
* Expose the data either on a API or 'Website'
* List all matches with teams (and scores) and filter by 'title', 'tournament', 'state', 'date_start__gte'and 'date_start_lte'
* Detail view of a match


#### Bonus
* Handle RabbitMQ exceptions (disconnect, service unreachable, etc.)
* Add logging through Python's 'logging'
* Serve API data through ElasticSearch (service description in docker-compose.yml)
* Try to merge similar items together - propose a way to connect them together

Preferred usage of Python packages:
- django
- django-restframework
- flask
- flask-restful
- pika
- elasticsearch-dsl
- django-elasticsearch-dsl
- django-elasticsearch-dsl-drf


## How to run

The application runs inside a docker container. The django application is served via gunicorn with a nginx server in front of it.

After cloning the repo, you can run in the terminal:
    
    ./local/build.sh (it builds the app container)
    ./local/start.sh (it runs the docker-compose command)

This should start the containers with the settings found in the ``.env`` file.
You can find a sample in the repo.
In the ``local`` folder there are some script to run:
    
    ```./local/runtests.sh``` to run the tests

## Miscellanea

#### Install git client Hooks

1. Open with a terminal and run
```bash
$ git config core.hooksPath git-hooks
```

The command above set git to use hooks saved in `git-hooks` instead of the default `.git/hooks/`.
This installation is required because [git doesn't track git client hooks.](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)

The pre-commit hook performs a check using flake8 with the same settings used during the deployment
The environment needs to be activated in order for the hook to work