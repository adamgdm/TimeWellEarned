.PHONY: up run-app

up:
	docker-compose up

run-app:
	python3 ./app.py