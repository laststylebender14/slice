FROM python:3.11.7-slim

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 6379

CMD [ "python3", "main.py" ]
