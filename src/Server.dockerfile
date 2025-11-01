FROM python:3

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./application /application/

WORKDIR /application/

ENV PYTHONPATH=/application

CMD python server/app.py 