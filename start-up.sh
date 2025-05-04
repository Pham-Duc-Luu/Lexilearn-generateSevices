#!/bin/bash

# export the enviroment variables


export $(cat .env | xargs)

source venv/bin/activate

fastapi dev app/main.py  --port $PORT