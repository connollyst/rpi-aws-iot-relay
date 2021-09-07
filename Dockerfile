FROM balenalib/raspberry-pi-debian:latest

MAINTAINER Sean Connolly <connolly.st@gmail.com>

RUN sudo apt-get update && \
    sudo apt-get install -y \
    cmake \
    python3-dev \
    python3-pip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt

COPY src/main/python/main.py /
COPY src/main/python/aws/AwsIotCore.py /aws/
COPY certs/ /certs/
CMD [ "python3", "./main.py" ]