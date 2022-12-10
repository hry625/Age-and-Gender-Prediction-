FROM python:3.9.12-slim

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN echo "Y" | apt-get install libglib2.0-0

COPY ./webservice/requirements.txt .

RUN python -m pip install --upgrade setuptools &&\
    python -m pip install cmake &&\
    pip install cython &&\
    pip install -r requirements.txt


COPY . .

CMD ["python","manage.py","runserver"]
