
docker-build:
	docker build -t ustwo/mastermind$(TAG) .
.PHONY: docker-build

docker-test:
	docker run -t ustwo/mastermind$(TAG) nosetests -s
.PHONY: docker-test

# CI fails with autoremove
docker-local-test:
	docker run --rm -t \
             --volume $(PWD):/usr/local/mastermind \
             ustwo/mastermind$(TAG) nosetests -s
.PHONY: docker-test

docker-version:
	docker run -t ustwo/mastermind$(TAG)
.PHONY: docker-test

docker-shell:
	docker run -t ustwo/mastermind$(TAG) bash
.PHONY: docker-test
