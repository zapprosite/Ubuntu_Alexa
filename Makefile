SHELL := /bin/bash
.PHONY: help venv install assistant-check assistant-dev

help:
	@echo "Targets:"; \
	echo "  venv               - cria .venv (python3 -m venv)"; \
	echo "  install            - instala requirements na .venv"; \
	echo "  assistant-check    - diagnostico (python check.py)"; \
	echo "  assistant-dev      - inicia o assistant em modo texto"

VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

venv:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PY) -m pip install --upgrade pip >/dev/null 2>&1 || true

install: venv
	@test -f requirements.txt && $(PIP) install -r requirements.txt || true

assistant-check: install
	@$(PY) check.py || true

assistant-dev: install
	@$(PY) assistant.py

