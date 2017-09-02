IMAGE_NAME=speech-api:latest

build:
	docker build -f Dockerfile -t ${IMAGE_NAME} .

run: YANDEX_KEY?='test'
run: PORT?=5000
run:
		docker run -ti --rm --name speech-api -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix${DISPLAY} --device /dev/snd -p ${PORT}:5000 -e YANDEX_KEY=${YANDEX_KEY} ${IMAGE_NAME}
