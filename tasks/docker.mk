
docker-build:
	docker build -t ustwo/mastermind .
.PHONY: docker-build

docker-test:
	docker run -t ustwo/mastermind nosetests -s
.PHONY: docker-test

# CI fails with autoremove
docker-local-test:
	docker run --rm -t \
             --volume $(PWD):/usr/local/mastermind \
             ustwo/mastermind nosetests -s
.PHONY: docker-test

docker-version:
	docker run -t ustwo/mastermind
.PHONY: docker-test
