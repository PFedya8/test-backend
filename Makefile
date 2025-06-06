.PHONY: run migrate test

install:
pip install -r requirements.txt

migrate:
python manage.py migrate

run:
python manage.py runserver 0.0.0.0:8000

test:
pytest -v
