FROM python:3.6-alpine

ENV YANDEX_KEY=test

RUN apk add -U ffmpeg
COPY app.py task.py requirements.txt /
pip install --upgrade -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
