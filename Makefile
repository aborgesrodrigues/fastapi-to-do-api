.PHONY: venv-dev

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    RM := echo y | del
    RM_DIR := rmdir /S /Q
    VENV_PY_VER := 3
    ACTIVATE := .\venv\Scripts\activate.bat
    DEACTIVATE := deactivate.bat
    PYTHON := python
    PIP := pip
else
	RM := rm -f ./
	RM_DIR := rm -rf ./
    detected_OS := $(shell uname)  # same as "uname -s"
    VENV_PY_VER := python3
    ACTIVATE := . ./venv/bin/activate
    DEACTIVATE := deactivate
    PYTHON := python
    PIP := pip
endif

venv: #
	uv sync

test: venv
	uv run pytest

start: 
	DB_HOST=localhost \
	uv run app.py

support:
	podman-compose up db filebeat elasticsearch kibana localstack

run:
	podman-compose up --build

clean:
	- podman-compose down
