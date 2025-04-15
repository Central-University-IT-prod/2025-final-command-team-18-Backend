FROM python:3.12

WORKDIR /app
COPY . /app
COPY tests/* /app/tests/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN export BASE_URL="http://localhost:8080/"

ENTRYPOINT ["pytest", "/app/tests"]