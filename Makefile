PROJECT = roipoly
TESTDIR = tests
EGG_INFO := $(subst -,_,$(PROJECT)).egg-info


init:
	pip install -r requirements.txt

install: init
	pip install .

test:
	pytest --cov=$(PROJECT) --cov-branch  --cov-report=term-missing

lint:
	flake8 $(PROJECT) tests

run_example:
	python examples/basic_example.py

dist:
	python setup.py sdist

upload: .git-no-changes
	twine upload dist/*

download:
	pip install $(PROJECT)

.git-no-changes:
	@if git diff --name-only --exit-code;         \
	then                                          \
		echo Git working copy is clean...;        \
	else                                          \
		echo ERROR: Git working copy is dirty!;   \
		echo Commit your changes and try again.;  \
		exit -1;                                  \
	fi;

clean-dist:
	-@rm -rf dist

clean-build:
	@find $(PROJECT) -name '*.pyc' -delete
	@find $(PROJECT) -name '__pycache__' -delete
	@find $(TESTDIR) -name '*.pyc' -delete 2>/dev/null || true
	@find $(TESTDIR) -name '__pycache__' -delete 2>/dev/null || true
	-@rm -rf $(EGG_INFO)
	-@rm -rf __pycache__

clean: clean-dist clean-build


.PHONY: init test install run_example lint upload .git-no-changes clean clean-dist clean-build
