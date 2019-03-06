PROJECT = roipoly

init:
	pip install -r requirements.txt

install: init
	pip install .

test:
	pytest --cov=$(PROJECT) --cov-branch  --cov-report=term-missing

lint:
	flake8 $(PROJECT) tests

run_example:
	python examples/example.py

.PHONY: init test install run_example lint