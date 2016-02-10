mastermind:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --url https://api.github.com/users/octocat/orgs
.PHONY: mastermind

mastermind-help:
	@$(shell pwd)/mastermind.py --help | $(LESS)
.PHONY: mastermind-help


mastermind-script:
	@$(shell pwd)/mastermind.py --quiet \
                              --script "$(shell pwd)/scripts/simple.py \
                                        https://api.github.com/users/octocat/orgs \
                                        $(shell pwd)/test/records/fake.json"
.PHONY: mastermind-script

mastermind-driver:
	@$(shell pwd)/mastermind.py --quiet \
                              --without-proxy-settings \
                              --with-driver \
                              --source-dir $(shell pwd)/test/records

.PHONY: mastermind-driver

mastermind-driver2:
	@$(shell pwd)/mastermind.py --quiet \
                              --with-driver \
                              --port 9090 \
                              --host 0.0.0.0 \
                              --source-dir $(shell pwd)/test/records
.PHONY: mastermind-driver2

mastermind-reverse-access:
	@$(shell pwd)/mastermind.py --quiet \
                              --with-driver \
                              --with-reverse-access \
                              --source-dir $(shell pwd)/test/records
.PHONY: mastermind-reverse-access


mastermind-error:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --script "$(shell pwd)/scripts/simple.py \
                                        https://api.github.com/users/octocat/orgs \
                                        $(shell pwd)/test/records/fake.json"
.PHONY: mastermind-error

schematics-architecture:
	@docker run --rm -it \
              -v $(PWD)/docs:/data \
              arnau/mermaid mermaid --png \
                                    -o schematics/ \
                                    schematics/architecture.mmd
schematics-driver:
	@docker run --rm -it \
              -v $(PWD)/docs:/data \
              arnau/mermaid mermaid --png \
                                    -o schematics/ \
                                    schematics/driver-sequence.mmd

schematics-driver-state:
	@docker run --rm -it \
              -v $(PWD)/docs:/data \
              arnau/mermaid mermaid --png \
                                    -o schematics/ \
                                    schematics/driver-stateful.mmd
