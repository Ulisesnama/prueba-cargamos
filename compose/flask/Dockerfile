FROM python:3.7-alpine

COPY . /app

WORKDIR /app

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
