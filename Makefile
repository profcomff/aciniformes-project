run:
	make run-api & make run-worker

run-api:
	source ./venv/bin/activate && uvicorn --reload --log-config logging_dev.conf aciniformes_backend.routes.base:app

run-worker:
	source ./venv/bin/activate && python -m aciniformes_backend worker --logger-config ./logging_dev.conf

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports aciniformes_backend
	isort aciniformes_backend
	black aciniformes_backend

format-dev:
	autoflake -r --in-place --remove-all-unused-imports tests
	isort tests
	black tests

	autoflake -r --in-place --remove-all-unused-imports migrations
	isort migrations
	black migrations

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-pinger_backend postgres:15

migrate:
	alembic upgrade head
