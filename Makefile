PS := ps
GREP := grep
PIP := pip
PYTHON := python
NOSE := nosetests
LESS := less
CURL := curl
GIT_BRANCH = $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null)
# VERSION ?= $(subst /,.,$(GIT_BRANCH))

version := v$(shell python mastermind/version.py)
artifact_osx = mastermind-$(version)-osx-amd64.tar.gz

install:
	pip install virtualenv
	virtualenv ./env-$(GIT_BRANCH) --always-copy
	. ./env-$(GIT_BRANCH)/bin/activate \
    && $(PIP) install -r requirements.txt
.PHONY: install

activate:
	@echo source ./env-$(GIT_BRANCH)/bin/activate
.PYTHON: activate

system-install:
	$(PYTHON) setup.py install
.PHONY: system-install


release: release-create release-artifacts
.PHONY: release

release-create:
	github-release release --user ustwo \
                         --repo mastermind \
                         --tag $(version)
.PHONY: release-create

release-artifacts: artifacts
	rm -rf build
	cp dist/mastermind dist/mastermind-$(version)
	cp dist/proxyswitch dist/proxyswitch-$(version)
	github-release upload --user ustwo \
                        --repo mastermind \
                        --tag $(version) \
                        --name $(artifact_osx) \
                        --file dist/$(artifact_osx)
.PHONY: release-artifacts

artifacts: bundle-mastermind bundle-proxyswitch dist/$(artifact_osx)
.PHONY: artifacts

dist/$(artifact_osx):
	@echo "Compressing"
	@cp LICENSE dist/LICENSE
	@cp NOTICE dist/NOTICE
	@cp README.md dist/README.md
	@tar -zcvf $@ -C dist/ mastermind \
                         proxyswitch \
                         LICENSE \
                         NOTICE \
                         README.md
	@echo "****************************************************************"
	@shasum -a 256 $@
	@du -sh $@
	@echo "****************************************************************"

release-expand:
	cd dist
	mkdir -p temp
	tar -zxvf $(tarball) -C temp/

release-info:
	github-release info --user ustwo --repo mastermind
.PHONY: release-info

release-delete:
	github-release delete --user ustwo --repo mastermind --tag $(version)
.PHONY: release-delete

bundle-mastermind:
	pyinstaller mastermind.spec
.PHONY: bundle-mastermind

bundle-proxyswitch:
	pyinstaller proxyswitch.spec
.PHONY: bundle-proxyswitch

homebrew-create:
	brew create tar --set-name mastermind

homebrew-install:
	brew install mastermind

homebrew-flush:
	rm -f /Library/Cache/Homebrew/mastermind*

test: docker-test
.PHONY: test

local-test: docker-local-test
.PHONY: local-test

raw-test:
	$(NOSE) -s
.PHONY: raw-test

include tasks/*.mk
