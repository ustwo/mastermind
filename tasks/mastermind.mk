mastermind:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --url https://api.github.com/users/octocat/orgs
.PHONY: mastermind

mastermind-help:
	@$(shell pwd)/mastermind.py --help | $(LESS)
.PHONY: mastermind-help


mastermind-driver:
	@$(shell pwd)/mastermind.py --quiet \
                              --without-proxy-settings \
                              --with-driver \
                              --no-upstream-cert \
                              --source-dir $(shell pwd)/test/records

.PHONY: mastermind-driver

mastermind-driver2:
	@$(shell pwd)/mastermind.py --quiet \
                              --with-driver \
                              --port 9090 \
                              --host 0.0.0.0 \
                              --source-dir $(shell pwd)/test/records
.PHONY: mastermind-driver2

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
