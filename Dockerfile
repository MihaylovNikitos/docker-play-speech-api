FROM python:3.6-alpine

ENV YANDEX_KEY=test

RUN apk add -U ffmpeg
RUN pip install yandex_speech flask pyglet
COPY app.py task.py /

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]
