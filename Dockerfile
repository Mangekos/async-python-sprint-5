FROM python:3.10.5-slim-buster

RUN apt update -y
RUN apt install -y python3

COPY requirements.txt requirements.txt

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "src/main.py", "db"]
