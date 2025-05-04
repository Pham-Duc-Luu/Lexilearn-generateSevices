
FROM python:3.10.17-slim-bullseye


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app

COPY ./public.pem /code/public.pem


CMD ["fastapi", "run", "app/main.py", "--port", "80"]