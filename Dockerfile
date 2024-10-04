FROM python

ENV PYTHONDONTWRITEBYTECCODE=1
ENV PYTHONNONBUFFERED=1

WORKDIR /app

COPY req.txt /app/


RUN pip install -r req.txt

COPY / /app/
