CONF = $(shell pwd)/examples/config/verbose.toml
mastermind:
	@$(shell pwd)/mastermind.py --config $(CONF) \
                              --no-upstream-cert
.PHONY: mastermind

mastermind-simple:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --url https://api.github.com/users/octocat/orgs
.PHONY: mastermind-simple

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
