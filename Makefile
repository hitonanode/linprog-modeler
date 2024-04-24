.PHONY: all mypy ruff-lint ruff-format test

all: mypy ruff-lint ruff-format test

mypy:
	poetry run mypy --strict .

ruff-lint:
	poetry run ruff check --fix .

ruff-format:
	poetry run ruff format .

test:
	poetry run pytest
