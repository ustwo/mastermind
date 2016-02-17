
docker-build:
	docker build -t ustwo/mastermind .
.PHONY: docker-build

docker-test:
	docker run -t ustwo/mastermind nosetests -s
.PHONY: docker-test

docker-version:
	docker run -t ustwo/mastermind
.PHONY: docker-test
