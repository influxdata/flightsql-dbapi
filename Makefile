SYSTEM_PYTHON3=python3
VENV=venv
BIN=$(VENV)/bin
PYTHON3=$(BIN)/python3

.DEFAULT_GOAL := build

.PHONY: build
build:
	$(PYTHON3) -m build

.PHONY: clean
clean:
	rm -rf $(VENV)
	rm -rf dist
	rm -rf __pycache__

.PHONY: proto
proto:
	protoc \
		--mypy_out=. \
		--python_out=. \
		flightsql/flightsql.proto

.PHONY: lint
lint: mypy flake8

.PHONY: flake8
flake8:
	$(PYTHON3) -m pflake8 .

.PHONY: mypy
mypy: venv
	$(PYTHON3) -m mypy -p flightsql --ignore-missing-imports

.PHONY: test
test: venv
	SQLALCHEMY_SILENCE_UBER_WARNING=1 $(PYTHON3) -m pytest --cov=flightsql -s

.PHONY: venv
venv: venv/touchfile

venv/touchfile: pyproject.toml
	$(SYSTEM_PYTHON3) -m venv $(VENV)
	. venv/bin/activate; $(PYTHON3) -m pip install '.[dev]'
	touch $(VENV)/touchfile
