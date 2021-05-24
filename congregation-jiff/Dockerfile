FROM ubuntu:18.04

WORKDIR /app

COPY . /app

# update apt-get, install curl and git
RUN apt-get update && \
    apt-get -qq -y install curl && \
    apt-get -y install git

# fetch node dependency
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash

# install node and python3.8
RUN apt-get install -y nodejs && \
    apt-get install -y --no-install-recommends python3.8 python3-pip python3.8-venv

# create python3.8 virtual environment
# and make it the default system version
ENV VIRTUAL_ENV=/opt/venv
RUN python3.8 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --upgrade pip

# install congregation
RUN cd /app && \
    git clone https://github.com/multiparty/congregation.git && \
    cd /app/congregation && \
    pip install -r requirements.txt && \
    python setup.py develop

# install curia
RUN cd /app && \
    git clone https://github.com/multiparty/curia.git && \
    cd /app/curia && \
    git checkout opt_append && \
    pip install -r requirements.txt && \
    python setup.py develop

# install jiff
RUN cd /app && \
    git clone https://github.com/multiparty/jiff.git && \
    cd /app/jiff && \
    npm install

RUN chmod +x /app/run.sh

CMD "./run.sh"