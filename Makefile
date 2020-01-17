.PHONY: analyze build

build:

analyze:
	pylint *.py
	shellcheck *.sh
