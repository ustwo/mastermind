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

http-proxyapp:
	@curl -I \
        --proxy http://localhost:8080 \
        -XGET http://proxyapp/foo

http-ustwo:
	@curl -I \
        --proxy http://localhost:8080 \
        -XGET http://ustwo.com

api-call:
	@curl -ki \
        --proxy http://localhost:8080 \
        -XGET https://api.github.com/users/octocat/orgs


http-local:
	@curl -I \
        --proxy http://localhost:8080 \
        -XGET http://localhost:8080


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



proxyapp:
	@mitmproxy -s ./proxyapp.py


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
