FROM python:3.10

WORKDIR /code

COPY ./BackendFastApi/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install pytest

COPY ./BackendFastApi/ /code/

ENV PYTHONPATH=/code

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
