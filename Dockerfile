FROM python:3.12

WORKDIR /code

COPY ../requirements.txt /code/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

RUN mkdir /.cache
RUN chmod 777 /.cache