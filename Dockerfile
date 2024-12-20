FROM python

ENV PYTHONDONTWRITEBYTECCODE=1
ENV PYTHONNONBUFFERED=1

WORKDIR /app

COPY req.txt /app/

ENV CURLOPT_SSL_VERIFYHOST=0
ENV CURLOPT_SSL_VERIFYPEER=0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r req.txt

COPY / /app/


