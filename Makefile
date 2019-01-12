init:
	pip install -r requirements.txt

install: init
	pip install .

test:
	nosetests -v tests

run_example:
	python examples/example.py

.PHONY: init test install run_example