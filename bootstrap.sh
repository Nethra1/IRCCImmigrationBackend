#!/bin/bash
export FLASK_APP=./api_mongo.py
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0