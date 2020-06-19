FROM ubuntu:18.04

RUN apt-get update && apt-get install -y sudo apt-transport-https ca-certificates curl gnupg-agent software-properties-common

RUN  apt-get update \
&& apt-get install -y unixodbc-dev gcc python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev g++ libgssapi-krb5-2

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17  mssql-tools


RUN apt-add-repository universe && apt-get update && apt-get install -y python3.8 python-pip


RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

COPY question3.py ./question3.py


CMD ["python","./question3.py"]