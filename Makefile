PYTHON = .venv/bin/python3
PIP = .venv/bin/pip


venv:
	python3.12 -m venv .venv
	$(PIP) install -r requirements.lock

install:
	$(PIP) install -r requirements.lock

db-up:
	cd docker-compose-dev && docker compose up -d --build

db-down:
	cd docker-compose-dev && docker compose down

create-superuser:
	$(PYTHON) manage.py createsuperuser

run:
	$(PYTHON) manage.py runserver

makemigrations:
	$(PYTHON) manage.py makemigrations

migrate:
	$(PYTHON) manage.py migrate

# lint:
# 	flake8 .

# collectstatic:
# 	$(PYTHON) manage.py collectstatic --noinput
#
# clean:
# 	find . -name "__pycache__" -exec rm -rf {} +
# 	find . -name "*.pyc" -exec rm -f {} +
