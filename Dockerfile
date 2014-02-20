FROM ubuntu
MAINTAINER Itxaka Serrano Garcia <itxakaserrano@gmail.com>

RUN apt-get update
RUN apt-get install -y git-core python-pip
RUN git clone https://github.com/Itxaka/Gobolino.git /var/www/

RUN pip install -r /var/www/web/requirements.txt
RUN sed -i "s/SECRET_KEY = ''/SECRET_KEY = '`tr -cd '[:alnum:]' < /dev/urandom | fold -w30 | head -n1`'/g" /var/www/web/config.py
RUN python /var/www/web/createuser.py admin admin
