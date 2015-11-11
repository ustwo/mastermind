PS := ps
GREP := grep
MITMPROXY := mitmproxy
MITMDUMP := mitmdump
PIP := pip
LESS := less


mitmcmd = $(MITMDUMP)
ifeq ($(INTERACTIVE), true)
  mitmcmd = $(MITMPROXY)
endif

.PHONY: test

install:
	$(PIP) install "git+https://github.com/ustwo/proxyswitch.git#egg=proxyswitch"

test:
	nosetests -s

include playground.mk

enable:
	@$(PWD)/proxyswitch.py --enable

disable:
	@$(PWD)/proxyswitch.py --disable


mastermind:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --url https://api.github.com/users/octocat/orgs

mastermind-script:
	@$(shell pwd)/mastermind.py --quiet \
                              --script "$(shell pwd)/proxyswitch/combo.py \
                                        https://api.github.com/users/octocat/orgs \
                                        $(shell pwd)/test/records/fake.json"


ps:
	@$(PS) -ef | $(GREP) $(mitmcmd) | $(LESS)

help:
	@$(mitmcmd) --help | $(LESS)
