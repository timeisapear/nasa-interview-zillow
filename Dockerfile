FROM python:3.12

RUN mkdir /packages

COPY ../requirements.txt /packages/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /packages/requirements.txt

WORKDIR /

RUN mkdir /.cache
RUN chmod 777 /.cache