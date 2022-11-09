# rhttp-shell

The project makes it possible to get a reverse shell on
difficult machines within a ctf environment by not using a basic tcp connection like other shells do.
Instead, it uses http/https to get and execute commands and perhaps evade detection and filters.

Until now there are two different modes:

* [wget.sh](wget.sh)
* [curl.sh](curl.sh)

The server can be started with:

```bash
# The server will generate a self signed cert for ssl
python3 main.py
# Now you can add commands and the client should 
# execute them and send the result back.
```

## Todo

### Know bugs

* path traversal does not work due nested execution of the commands
