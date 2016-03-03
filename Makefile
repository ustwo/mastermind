PS := ps
GREP := grep
PIP := pip
PYTHON := python
NOSE := nosetests
LESS := less
CURL := curl
GIT_BRANCH = $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null)
# VERSION ?= $(subst /,.,$(GIT_BRANCH))

install:
	$(PIP) install -r requirements.txt
.PHONY: install

system-install:
	$(PYTHON) setup.py install
.PHONY: system-install

release: version := v$(shell python mastermind/version.py)
release: bundle-mastermind bundle-proxyswitch
	rm -rf build
	cp dist/mastermind dist/mastermind-$(version)
	cp dist/proxyswitch dist/proxyswitch-$(version)
	git tag $(version)
	git push origin $(GIT_BRANCH)
	github-release release --user ustwo \
                         --repo mastermind \
                         --tag $(version) \
                         --pre-release
	github-release upload --user ustwo \
                        --repo mastermind \
                        --tag $(version) \
                        --name "mastermind-osx-amd64" \
                        --file dist/mastermind
	github-release upload --user ustwo \
                        --repo mastermind \
                        --tag $(version) \
                        --name "proxyswitch-osx-amd64" \
                        --file dist/proxyswitch
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
