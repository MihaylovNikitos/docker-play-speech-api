IMAGE_NAME=speech-api:latest

docker_build:
	docker build -f Dockerfile -t ${IMAGE_NAME} .

docker_run: YANDEX_KEY?='test'
docker_run: APP_PORT?=5000
dcoker_run:
		docker run -ti --rm --name speech-api -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix${DISPLAY} --device /dev/snd -p ${APP_PORT}:5000 -e YANDEX_KEY=${YANDEX_KEY} ${IMAGE_NAME}

run: YANDEX_KEY?='test'
run: APP_PORT?=5000
run:
	export APP_PORT=${APP_PORT} ; \
	export YANDEX_KEY=${YANDEX_KEY} ; \
	pip3 install --upgrade -r requirements.txt ; \
	python3 app.py
