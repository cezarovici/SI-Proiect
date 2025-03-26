FROM python:3.9

WORKDIR /code

COPY ./BackendFastApi/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./BackendFastApi/ /code/app

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "8000"]

EXPOSE 8000
