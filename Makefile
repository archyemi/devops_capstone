## The Makefile includes instructions on environment setup and lint tests
# Create and activate a virtual environment
# Install dependencies in requirements.txt
# Dockerfile should pass hadolint
# app.py should pass pylint
# (Optional) Build a simple integration test

setup:
	# Create python virtualenv & source it
	python3 -m venv venv

install:
	# This should be run from inside a virtualenv
	pip install --upgrade pip &&\
		pip install -r ./techtrends/requirements.txt
    
lint:
	# This is linter for Dockerfiles
	hadolint Dockerfile
	# This is a linter for Python source code linter: https://www.pylint.org/
	# This should be run from inside a virtualenv
	pylint --disable=R,C,W1203,W1309,W0603,E1101,W0611,W0311,W0621 ./techtrends/app.py

all: install lint setup