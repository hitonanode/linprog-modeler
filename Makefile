.PHONY: ruff mypy format

mypy:
	poetry run mypy --strict .

ruff:
	poetry run ruff format .

format:
	make mypy
	make ruff
