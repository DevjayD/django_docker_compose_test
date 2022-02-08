# pull official base image
FROM python:3.9

#Get initial apps
RUN apt install bash git

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install pip==21.2.4

# copy project
COPY . /app

RUN pip install  --default-timeout=100 -r requirements.txt
