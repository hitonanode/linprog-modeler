.PHONY: ruff mypy format test

all: ruff mypy format test

mypy:
	poetry run mypy --strict .

ruff:
	poetry run ruff format .

format:
	make mypy
	make ruff

test:
	poetry run pytest
