#!/bin/bash

# export the enviroment variables


export $(cat .env | xargs)

pip freeze > requirements.txt

# Build docker image 
# sudo docker build -t lexilearn-generate-text-service .
# sudo docker compose up -d

# Build docker hub
# sudo docker build -t pdluu/lexilearn-generate-text-service .
# sudo docker push pdluu/lexilearn-generate-text-service


source venv/bin/activate
#
fastapi dev app/main.py  --port $PORT
# uvicorn app.main:app --reload --port $PORT
