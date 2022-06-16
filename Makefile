.PHONY: analyze build

build:

check:
	echo "No tests defined"

prereqs:
	pip3 install paho-mqtt

analyze:
	pylint *.py
	shellcheck *.sh
