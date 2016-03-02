PS := ps
GREP := grep
PIP := pip
PYTHON := python
NOSE := nosetests
LESS := less
CURL := curl

install:
	$(PIP) install -r requirements.txt
.PHONY: install

system-install:
	$(PYTHON) setup.py install
.PHONY: system-install

bundle: bundle-mastermind bundle-proxyswitch
.PHONY: bundle

bundle-mastermind:
	pyinstaller --onefile mastermind.spec
	rm -rf build
.PHONY: bundle-mastermind

bundle-proxyswitch:
	pyinstaller proxyswitch.spec
.PHONY: bundle-proxyswitch

test: docker-test
.PHONY: test

local-test: docker-local-test
.PHONY: local-test

raw-test:
	$(NOSE) -s
.PHONY: raw-test

include tasks/*.mk
