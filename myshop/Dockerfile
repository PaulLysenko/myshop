FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y netcat-traditional mc dos2unix

WORKDIR /app

COPY myshop/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY myshop/entrypoint.sh /usr/local/bin/

RUN dos2unix /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]