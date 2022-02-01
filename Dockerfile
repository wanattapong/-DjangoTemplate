FROM python:3.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app

COPY ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install mysqlclient
RUN pip install -r /app/requirements.txt
RUN pip3 uninstall avro-python3 -y && pip install avro-python3==1.8.2

COPY . /app/src/
WORKDIR /app/src/

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]