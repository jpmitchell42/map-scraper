FROM amazonlinux:2018.03

RUN yum -y install git \
    python36 \
    python36-pip \
    zip \
    && yum clean all

RUN python3 -m pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt


