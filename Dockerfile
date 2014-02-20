FROM ubuntu
MAINTAINER Itxaka Serrano Garcia <itxakaserrano@gmail.com>

RUN apt-get update
RUN apt-get install -y git-core python-pip


RUN git clone https://github.com/Itxaka/Gobolino.git /var/www/
RUN pip install -r /var/www/requirements.txt
RUN ls -ltr /var/www
RUN PASS=`tr -cd '[:alnum:]' < /dev/urandom | fold -w30 | head -n1`
ENV PASS caca
RUN sed -e 's/SECRET_KEY = ""/$PASS/g' /var/www/config.py
