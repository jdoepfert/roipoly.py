PROJECT = roipoly

init:
	pip install -r requirements.txt

install: init
	pip install .

test:
	nosetests -v tests

lint:
	flake8 $(PROJECT)

run_example:
	python examples/example.py

.PHONY: init test install run_example