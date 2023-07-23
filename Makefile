run:
	source ./venv/bin/activate && uvicorn --reload --log-config logging_dev.conf aciniformes_backend.routes.base:app

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

atomic-format:
	autoflake -r --in-place --remove-all-unused-imports ./$(module)
	isort ./$(module)
	black ./$(module)

format:
	make atomic-format module=pinger_backend
	make atomic-format module=aciniformes_backend
	make atomic-format module=settings.py

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-pinger_backend postgres:15

migrate:
	alembic upgrade head
