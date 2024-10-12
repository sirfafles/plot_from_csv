FROM python:3.11

WORKDIR /plot-from-csv/backend/src

COPY ./requirements.txt /plot-from-csv/backend/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r /plot-from-csv/backend/requirements.txt

RUN mkdir cache

COPY ./src /plot-from-csv/backend/src

EXPOSE 8000

CMD ["python", "-m", "app"]
