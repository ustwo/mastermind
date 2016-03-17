test-schema-errors:
	@curl --proxy http://localhost:8080 \
        -XGET "http://proxapp:5000/fake/exceptions/?uri=https://api.github.com/users/arnau/orgs"


test-api-call:
	@curl -ki \
        --proxy http://localhost:8080 \
        -XGET https://api.github.com/users/octocat/orgs

test-api-call2:
	@$(call driver_start, fake)
	@curl -ki \
        --proxy http://localhost:8080 \
        -XGET https://api.github.com/users/arnau/orgs
	@$(call driver_stop)

test-delay:
	@$(call driver_start, skip)
	@curl -i --proxy http://localhost:8080 \
           -XGET http://localhost:8000/slow/
	@$(call driver_stop)

test-200:
	@$(call driver_start, skip)
	@curl -i --proxy http://localhost:8080 \
           -XGET http://localhost:8000
	@$(call driver_stop)

test-201:
	@$(call driver_start, skip)
	@curl -i --proxy http://localhost:8080 \
           -XPOST http://localhost:8000/
	@$(call driver_stop)


test-200-2:
	@curl -i --proxy http://0.0.0.0:9090 \
           -XGET http://localhost:8000


test-500:
	@$(call driver_start, skip)
	@curl -i --proxy http://localhost:8080 \
           -XGET http://localhost:8000/500/
	@$(call driver_stop)

test-400:
	@$(call driver_start, skip)
	@curl -i --proxy http://localhost:8080 \
           -XGET http://localhost:8000/400/
	@$(call driver_stop)

test-skipcert:
	@$(call driver_start, skip)
	@curl -I \
        --cacert ~/.mitmproxy/mitmproxy-ca-cert.pem \
        --proxy http://localhost:8080 \
        -XGET "https://ustwo.com/what-we-do/?foo=1&bar=baz"
	@$(call driver_stop)

test-templ:
	@$(call driver_start, skip)
	@curl -i \
        --proxy http://localhost:8080 \
        -XGET http://localhost:8000/people/123?q=1
	@$(call driver_stop)


skip-start:
	@$(call driver_start, skip)

skip-stop:
	@$(call driver_stop, skip)

define driver_start
  curl -L --proxy http://localhost:8080 \
          -XGET http://proxapp:5000/$(strip $1)/start/ > /dev/null 2>&1
endef

define driver_stop
  curl -L --proxy http://localhost:8080 \
          -XGET http://proxapp:5000/stop/ > /dev/null 2>&1
endef
