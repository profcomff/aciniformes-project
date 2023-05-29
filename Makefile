run:
	source ./venv/bin/activate && uvicorn --reload --log-config logging_dev.conf aciniformes_backend.routes.base:app

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports ./pinger_backend
	isort ./pinger_backend
	black ./pinger_backend

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-pinger_backend postgres:15

migrate:
	alembic upgrade head
