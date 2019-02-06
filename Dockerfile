FROM ubuntu:16.04
MAINTAINER Daniel Beßler, danielb@cs.uni-bremen.de

# AR-Helper required services for this Dockerfile: ?with-service=apt&with-service=pip&with-service=npm
ARG AR=""
ADD $AR /tmp/ar-helper
RUN test -f /tmp/ar-helper && chmod +x /tmp/ar-helper && /tmp/ar-helper || true

# install python and flask
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update &&\
    DEBIAN_FRONTEND=noninteractive\
    apt-get -qq install -y -q curl python-all python-pip python-dev wget gcc imagemagick mongodb libffi-dev libpq-dev netcat\
                              subversion git\
                              python-tornado\
                              nodejs nodejs-legacy npm &&\
    rm -rf /var/lib/apt/lists/*

ADD requirements.txt /tmp/webapp_requirements.txt
RUN pip install -r /tmp/webapp_requirements.txt
WORKDIR /opt/webapp

# flag used in nginx configuration
ENV OPEN_EASE_WEBAPP true

# work as user 'ros'
RUN useradd -m -d /home/ros -p ros ros && chsh -s /bin/bash ros
ENV HOME /home/ros

## install npm dendencies
RUN mkdir /tmp/npm
ADD ./webrob/static/index.js ./webrob/static/package.json /tmp/npm/
RUN cd /tmp/npm && npm install && npm run build && chown -R ros:ros /tmp/npm

## copy this folder to the container
ADD . /opt/webapp/
RUN chown -R ros:ros /opt/webapp/

USER ros

# install JS libraries using npm
# TODO why need to copy?
# RUN cd /opt/webapp/webrob/static && npm install
RUN mv /tmp/npm/openease*.js /opt/webapp/webrob/static/

RUN cd /home/ros
# Expose volumes for maintenance
VOLUME /opt/webapp/

EXPOSE 5000

CMD ["python", "runserver.py"]
