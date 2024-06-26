.ONESHELL:
IMAGE=secret-santa-django

dev: kill build run watch

watch:
	LATEST_CONTAINER=$$(docker ps -a | grep -w $(IMAGE) | head -n 1 | cut -d' ' -f1)
	watch --color -n .2 "docker logs $$LATEST_CONTAINER 2>&1 | tail -n $$(($$(tput lines) - 3))"

build:
	docker build . -t $(IMAGE)

run: kill build
	docker run -d \
	-p 8080:8080 \
	--mount type=bind,src=./db.sqlite3,target=/app/db.sqlite3 \
	$(IMAGE)

kill:
	docker ps | grep -w $(IMAGE) | cut -d' ' -f1 | xargs -r docker kill

logs:
	LATEST_CONTAINER=$$(docker ps -a | grep -w $(IMAGE) | head -n 1 | cut -d' ' -f1)
	docker logs $$LATEST_CONTAINER

live:
	python manage.py runserver 8080
