SHELL := /bin/bash
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR := $(realpath $(dir $(MAKEFILE_PATH)))
CWD := $(notdir $(patsubst %/,%,$(dir $(MAKEFILE_PATH))))
VENV_DIR := $(MAKEFILE_DIR)/.venv
REQ_FP := $(MAKEFILE_DIR)/requirements.txt

LOCAL_PYPI_FP := $(MAKEFILE_DIR)/local_pypi_dir.txt
LOCAL_PYPI_DIR := $(shell cat ${LOCAL_PYPI_FP})
PKG_NAME := topshelfsoftware_aws_util
PKG_VER := 0.1.1

# function to activate the python virtual env
activate = . $(VENV_DIR)/bin/activate && $1

.PHONY: build copy install

all: build copy

build:
	$(call activate,poetry build --format wheel)

copy:
	cp $(MAKEFILE_DIR)/dist/$(PKG_NAME)-$(PKG_VER)*.whl $(LOCAL_PYPI_DIR)

install:
	@echo "Setting up Python virtual env"
	python3.9 -m venv $(VENV_DIR)
	
	@echo "Upgrading pip"
	$(call activate,python -m pip install --upgrade pip)

	@echo "Installing project dependencies"
	$(call activate,python -m pip install -r $(REQ_FP))
