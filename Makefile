install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

lint:
	uv run flake8 page_analyzer/

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf page_analyzer/__pycache__
	rm -rf .ruff_cache