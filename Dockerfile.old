FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get install -y libsnappy-dev
RUN pip install -r requirements.txt
COPY . /code/
