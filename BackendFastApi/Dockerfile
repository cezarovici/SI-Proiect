FROM python:3.9

WORKDIR /code

COPY ./BackendFastApi/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install pytest

COPY ./BackendFastApi/ /code/app

EXPOSE 8000

#RUN pytest app/test_main.py -v || exit 1

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
