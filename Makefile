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


install:
	$(PIP) install "git+https://github.com/ustwo/proxyswitch.git#egg=proxyswitch"

include playground.mk

enable:
	@$(PWD)/proxyswitch.py --enable

disable:
	@$(PWD)/proxyswitch.py --disable

# Mastermind without mastermind
combo:
	$(mitmcmd) --host \
             --script "$(shell pwd)/proxyswitch/combo.py \
                       https://api.github.com/users/octocat/orgs \
                       $(shell pwd)/test/records/fake.json"

mastermind:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              https://api.github.com/users/octocat/orgs


ps:
	@$(PS) -ef | $(GREP) $(mitmcmd) | $(LESS)

help:
	@$(mitmcmd) --help | $(LESS)
