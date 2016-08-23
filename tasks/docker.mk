DOCKER := docker
DOCKER_TASK := $(if $(CI), $(DOCKER) run -it, $(DOCKER) run --rm -it)

DOCKER_IMAGE = ustwo/mastermind$(TAG)

docker-build:
	@$(DOCKER) build -t $(DOCKER_IMAGE) .
.PHONY: docker-build

docker-test:
	@$(DOCKER_TASK) $(DOCKER_IMAGE) py.test -v test
.PHONY: docker-test

docker-local-test:
	@$(DOCKER_TASK) --volume $(PWD):/usr/local/mastermind \
                  $(DOCKER_IMAGE) py.test -v test
.PHONY: docker-local-test

docker-version:
	@$(DOCKER_TASK) $(DOCKER_IMAGE)
.PHONY: docker-version

docker-shell:
	@$(DOCKER_TASK) $(DOCKER_IMAGE) bash
.PHONY: docker-shell
