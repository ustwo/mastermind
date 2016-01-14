.PHONY: \
  mastermind \
  mastermind-help \
  mastermind-script \
  mastermind-driver \
  mastermind-error \
  test-api-call

mastermind:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --url https://api.github.com/users/octocat/orgs

mastermind-help:
	@$(shell pwd)/mastermind.py --help | $(LESS)


mastermind-script:
	@$(shell pwd)/mastermind.py --quiet \
                              --script "$(shell pwd)/scripts/simple.py \
                                        https://api.github.com/users/octocat/orgs \
                                        $(shell pwd)/test/records/fake.json"

mastermind-driver:
	@$(shell pwd)/mastermind.py --quiet \
                              --with-driver \
                              --source-dir $(shell pwd)/test/records

mastermind-reverse-access:
	@$(shell pwd)/mastermind.py --quiet \
                              --with-driver \
                              --with-reverse-access \
                              --source-dir $(shell pwd)/test/records


mastermind-error:
	@$(shell pwd)/mastermind.py --quiet \
                              --response-body $(shell pwd)/test/records/fake.json \
                              --script "$(shell pwd)/scripts/simple.py \
                                        https://api.github.com/users/octocat/orgs \
                                        $(shell pwd)/test/records/fake.json"


test-api-call:
	@curl -ki \
        --proxy http://localhost:8080 \
        -XGET https://api.github.com/users/octocat/orgs

test-api-call2:
	@curl -ki \
        --proxy http://localhost:8080 \
        -XGET https://api.github.com/users/arnau/orgs
