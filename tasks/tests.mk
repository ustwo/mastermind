test-api-call:
	@curl -ki \
        --proxy http://localhost:8080 \
        -XGET https://api.github.com/users/octocat/orgs

test-api-call2:
	@curl -ki \
        --proxy http://localhost:8080 \
        -XGET https://api.github.com/users/arnau/orgs


test-200:
	@$(call driver_start, skip)
	@curl -i --proxy http://localhost:8080 \
           -XGET http://localhost:8000
	@$(call driver_stop)

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


define driver_start
  curl -L --proxy http://localhost:8080 \
          -XGET http://proxapp:5000/$(strip $1)/start/
endef

define driver_stop
  curl -L --proxy http://localhost:8080 \
          -XGET http://proxapp:5000/stop/
endef
