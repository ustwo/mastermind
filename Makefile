install:
	pip install git+https://github.com/arnau/proxyswitch.git#egg=proxyswitch

enable:
	@$(PWD)/proxyswitch/__init__.py --enable

disable:
	@$(PWD)/proxyswitch/__init__.py --disable

toggle:
	@$(PWD)/proxyswitch/__init__.py

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
	@curl -I \
        --proxy http://localhost:8080 \
        -XGET http://github.com

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

# --limit "~d ustwo.com" \

http-ustwo:
	@curl -I \
        --proxy http://localhost:8080 \
        -XGET http://ustwo.com

http-local:
	@curl -I \
        --proxy http://localhost:8080 \
        -XGET http://localhost:8080

record:
	@mitmdump -w recorded-request

replay:
	@mitmdump -c recorded-request


transparent:
	@mitmproxy --transparent \
             --verbose \
             --host \
             --eventlog

mock:
	@$(PWD)/mock.py

ps:
	@ps -ef | grep mitm | less

help:
	@mitmproxy --help | less

help-dump:
	@mitmdump --help | less

pf:
	@sudo pfctl -s all | less
