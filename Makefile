PYTHON3=python3

.DEFAULT_GOAL := build

.PHONY: build
build:
	$(PYTHON3) -m build

.PHONY: clean
clean:
	rm -rf dist
	rm -rf venv
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
	. venv/bin/activate; $(PYTHON3) -m pflake8 .

.PHONY: mypy
mypy: venv
	. venv/bin/activate; $(PYTHON3) -m mypy -p flightsql --ignore-missing-imports

.PHONY: test
test: venv
	. venv/bin/activate; pytest

activate: venv

.PHONY: venv
venv: venv/touchfile

venv/touchfile: pyproject.toml
	test -d venv || $(PYTHON3) -m venv venv
	. venv/bin/activate; $(PYTHON3) -m pip install '.[dev]'
	touch venv/touchfile
