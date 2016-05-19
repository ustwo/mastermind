FROM python:2.7-slim
MAINTAINER Arnau Siches <arnau@ustwo.com>

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHON /usr/bin/python2.7
ENV LANG en_US.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update \
 && apt-get install -qq -y --no-install-recommends \
      build-essential \
      libffi-dev \
      libxml2-dev \
      libxslt1-dev \
      libjpeg-dev \
      git \
      zlib1g-dev \
      libssl-dev \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --upgrade pip


COPY requirements.txt /usr/local/mastermind/requirements.txt

WORKDIR /usr/local/mastermind

RUN pip install -r requirements.txt \
 && rm -rf ~/.cache/pip /tmp/pip_build_root

COPY . /usr/local/mastermind

RUN python setup.py install

CMD ["mastermind", "--version"]
