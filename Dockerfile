FROM python:3.12
LABEL authors="OldestSalt"

COPY requirements.txt .

RUN apt-get update
RUN pip3 install --no-cache-dir --no-deps -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "./main.py"]
