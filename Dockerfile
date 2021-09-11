FROM python:3.8-slim-buster


ENV PYTHONUNBUFFERD=1

RUN mkdir /django
WORKDIR /django
COPY requirements.txt /django/
COPY . /django
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt



