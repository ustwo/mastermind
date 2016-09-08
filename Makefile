GIT_BRANCH = $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null)
ENV = ./env-$(GIT_BRANCH)
ifdef VIRTUAL_ENV
  ENV_BIN = $(ENV)/bin/
endif

ifneq ("$(GIT_BRANCH)", "master")
  BRANCH_VERSION = cat mastermind/version.py | sed -E "s/^IVERSION.+$$/IVERSION = ('$(GIT_BRANCH)')/"
endif

version := v$(shell python mastermind/version.py)
artifact_osx = mastermind-$(version)-osx-amd64.tar.gz

default: meta install
.PHONY: default

clean:
	find . -name \*.pyc -delete
.PHONY: clean

meta:
	pip install virtualenv
.PHONY: meta

env:
	virtualenv $(ENV) --always-copy
.PHONY: env

# Note: Downgrades setuptools to 19.2 so PyInstaller 3.1 does not fail.
# Note: PyInstaller 3.2 fails silently. No apparent reason.
install:
	. $(ENV)/bin/activate && pip install -r requirements.txt
	. $(ENV)/bin/activate && pip install setuptools==19.2
.PHONY: install

activate:
	@echo source $(ENV)/bin/activate
.PYTHON: activate

system-install:
	python setup.py install
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
	$(ENV_BIN)pyinstaller mastermind.spec
.PHONY: bundle-mastermind

bundle-proxyswitch:
	$(ENV_BIN)pyinstaller proxyswitch.spec
.PHONY: bundle-proxyswitch

homebrew-create:
	brew create tar --set-name mastermind

homebrew-install:
	brew install mastermind

homebrew-flush:
	rm -f /Library/Cache/Homebrew/mastermind*

test: docker-test
.PHONY: test

raw-test: clean
	py.test -v test
	rm -rf /var/tmp/mastermind*
.PHONY: raw-test

lint:
	flake8 --jobs 8 --count mastermind test

include tasks/*.mk
