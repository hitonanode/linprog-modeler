.PHONY: ruff mypy format

mypy:
	poetry run mypy .

ruff:
	poetry run ruff format .

format:
	make mypy
	make ruff
