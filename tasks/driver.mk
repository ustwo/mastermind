###############################################################################
# The driver tasks expect mastermind to be runnin with the driver mode.  See
# the `mastermind-driver` task.
###############################################################################

.PHONY: \
  driver-start \
  driver-stop

driver-start:
	@$(CURL) --proxy http://localhost:8080 \
           -XGET http://proxapp:5000/fake/start

driver-stop:
	@$(CURL) --proxy http://localhost:8080 \
           -XGET http://proxapp:5000/stop

driver-stop2:
	@$(CURL) -XGET http://0.0.0.0:5000/stop \
           --proxy http://localhost:8080
