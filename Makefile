PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

run:
	uv run hexlet-python-package

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=hexlet_python_package --cov-report xml

lint:
	uv run ruff check

check: test lint

build:
	./build.sh    

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
    
.PHONY: install test lint check build start dev run test-coverage render-start