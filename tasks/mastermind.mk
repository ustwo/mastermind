CONF = $(shell pwd)/examples/config/verbose.toml

mastermind:
	@echo $(CONF)
	@$(shell pwd)/mastermind.py --config $(CONF) \
                              --no-upstream-cert
.PHONY: mastermind

mastermind-driver:
	@echo $(CONF)
	@$(shell pwd)/mastermind.py --with-driver \
                              --source-dir $(shell pwd)/test/records \
                              --no-upstream-cert
.PHONY: mastermind-driver

mastermind-simple:
	@$(shell pwd)/mastermind.py -vvvvvv \
                              --port 8900 \
                              --without-proxy-settings \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --url https://api.github.com/users/octocat/orgs
.PHONY: mastermind-simple

mastermind-simple-settings:
	@$(shell pwd)/mastermind.py -vvvvvv \
                              --port 8900 \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --url https://api.github.com/users/octocat/orgs
.PHONY: mastermind-simple-settings


mastermind-simple-broken1:
	@$(shell pwd)/mastermind.py \
                              --port 8900 \
                              --without-proxy-settings \
                              --response-body $(shell pwd)/test/records/fake.json \
                              https://api.github.com/users/octocat/orgs
.PHONY: mastermind-simple-broken1

mastermind-simple-broken2:
	@$(shell pwd)/mastermind.py \
                              --port 8900 \
                              --without-proxy-settings \
                              --url https://api.github.com/users/octocat/orgs
.PHONY: mastermind-simple-broken2


mastermind-bin:
	@$(shell pwd)/dist/mastermind --config $(CONF) \
                                --no-upstream-cert
.PHONY: mastermind-bin

mastermind-error:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --script "$(shell pwd)/scripts/simple.py \
                                        https://api.github.com/users/octocat/orgs \
                                        $(shell pwd)/test/records/fake.json"
.PHONY: mastermind-error

mastermind-error2:
	@$(shell pwd)/mastermind.py --with-driver \
                              --without-proxy-settings \
                              --source-dir $(shell pwd)/test/records \
                              --response-body $(shell pwd)/test/records/fake.json
.PHONY: mastermind-error2

schematics: schematics-architecture schematics-driver schematics-driver-state
.PHONY: schematics

schematics-architecture:
	@docker run --rm -it \
              -v $(PWD)/docs:/data \
              arnau/mermaid mermaid --png \
                                    -o schematics/ \
                                    schematics/architecture.mmd
.PHONY: schematics-architecture

schematics-driver:
	@docker run --rm -it \
              -v $(PWD)/docs:/data \
              arnau/mermaid mermaid --png \
                                    -o schematics/ \
                                    schematics/driver-sequence.mmd
.PHONY: schematics-driver

schematics-driver-state:
	@docker run --rm -it \
              -v $(PWD)/docs:/data \
              arnau/mermaid mermaid --png \
                                    -o schematics/ \
                                    schematics/driver-stateful.mmd
.PHONY: schematics-driver-state
