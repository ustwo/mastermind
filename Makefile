enable:
	@$(PWD)/proxyswitch.py --enable

disable:
	@$(PWD)/proxyswitch.py --disable

toggle:
	@$(PWD)/proxyswitch.py

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

# Expected: 301
http-github:
	@curl -I \
        --proxy http://localhost:8080 \
        -XGET http://github.com

simple:
	@mitmproxy --verbose \
             --host \
             --eventlog

script:
	@mitmproxy --host \
             --verbose \
             --anticache \
             --eventlog \
             --script $(PWD)/example.py

transparent:
	@mitmproxy --transparent \
             --verbose \
             --host \
             --eventlog


ps:
	@ps -ef | grep mitm | less

help:
	@mitmproxy --help | less

help-dump:
	@mitmdump --help | less

pf:
	@sudo pfctl -s all | less
