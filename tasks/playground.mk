# Expected: 200
https-github:
	@curl -I \
        -vvvv \
        --insecure \
        --proxy http://localhost:8080 \
        -XGET https://github.com

# Expected: 302
https-google:
	@curl -I \
        -vvvv \
        --proxy http://localhost:8080 \
        -XGET https://google.com

# Expected: 302
http-github:
	@curl -i \
        --proxy http://localhost:8080 \
        -XGET http://github.com

http-ustwo:
	@curl -I \
        --proxy http://localhost:8080 \
        -XGET http://ustwo.com


simple:
	@mitmproxy --verbose \
             --host \
             --eventlog

d-simple:
	@mitmdump --verbose \
            --host

w-simple:
	@mitmweb --verbose \
           --host \
           --wport 9980 \
           --wdebug

d-script:
	@mitmdump --verbose \
            --host \
            --script $(PWD)/sandbox/example.py

p-script:
	@mitmproxy --verbose \
             --host \
             --script "$(PWD)/sandbox/example.py"

record:
	@mitmdump -w recorded-request

replay:
	@mitmdump -c recorded-request

transparent:
	@mitmproxy --transparent \
             --verbose \
             --host \
             --eventlog

pf:
	@sudo pfctl -s all | $(LESS)
