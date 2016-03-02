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

release: bundle-mastermind bundle-proxyswitch
	rm -rf build
	ln -sf $(shell ls -LArt dist \
               | grep mastermind \
               | tail -1) dist/mastermind
	ln -sf $(shell ls -LArt dist \
               | grep proxyswitch \
               | tail -1) dist/proxyswitch
	git tag v$(shell python mastermind/version.py)
.PHONY: release

bundle-mastermind:
	pyinstaller mastermind.spec
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
