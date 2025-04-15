FROM python:3.12-alpine3.21

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

RUN apk add --no-cache curl

COPY . .
RUN dos2unix prod.start.sh
RUN dos2unix start.sh

ENTRYPOINT ["sh", "/usr/src/app/prod.start.sh" ]