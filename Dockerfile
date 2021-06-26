FROM python:3.9-slim as executor
ENV PYTHONUNBUFFERED=1
RUN sed -Ei 's/main$/main contrib/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN apt-get -y install mysql-server
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -y git default-libmysqlclient-dev
RUN apt-get -y install docker-ce
RUN apt-get install -y gcc g++

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN pip install mysqlclient
RUN mkdir /templates

ENV ENVIRONMENT=docker

COPY . /executor

WORKDIR /executor

#RUN python manage.py makemigrations
#RUN python manage.py migrate
#RUN python manage.py collectstatic --clear --noinput

EXPOSE 8000
