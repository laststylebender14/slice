FROM python:3.11.7-slim

WORKDIR /app

COPY . .

EXPOSE 6379

CMD [ "python3", "main.py" ]
