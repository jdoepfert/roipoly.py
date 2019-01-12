PROJECT = roipoly

init:
	pip install -r requirements.txt

install: init
	pip install .

test:
	nosetests -v tests --with-coverage --cover-package=$(PROJECT) --cover-min-percentage=40

lint:
	flake8 $(PROJECT)

run_example:
	python examples/example.py

.PHONY: init test install run_example lint