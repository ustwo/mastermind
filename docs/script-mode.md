### Script

**Use this option if you *know* what you are doing**.

The script mode expects a [mitmproxy inline script][mitm-script]:

```sh
sudo mastermind --script $(pwd)/myscript.py
```

Or pass parameters to your script the same way mitmproxy does:

```sh
sudo mastermind --script "$(pwd)/myscript.py param1 param2"
```

[mitm-script]: http://docs.mitmproxy.org/en/stable/scripting/inlinescripts.html
