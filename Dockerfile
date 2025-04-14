FROM python:latest

WORKDIR /src

COPY requirements.txt requirements.txt

COPY alembic.ini alembic.ini

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src .

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "core/logging.yaml"]