import os
import ssl
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer


class SecureServer(BaseHTTPRequestHandler):
    # Kind of hacky solution but overwrites the log output function
    def log_request(self, code):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header('python 3', 'text/html')
        self.end_headers()
        message = input("$ ")
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        if 'Content-Length' in self.headers:
            varlen = int(self.headers['Content-Length'])
            print(self.rfile.read(varlen).decode())


if not os.path.exists('local.pem'):
    subprocess.Popen(
        'openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -subj "/C=AU/ST=Some-State/L=Some-City/O=MeMyselfAndI/OU=Org/CN=localhost" -nodes',
        shell=True).wait()
    subprocess.Popen('cat cert.pem key.pem > local.pem', shell=True).wait()
    subprocess.Popen('rm cert.pem key.pem', shell=True).wait()

server_address = ("0.0.0.0", 4443)
httpd = HTTPServer(server_address, SecureServer)
httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile="local.pem", ssl_version=ssl.PROTOCOL_TLSv1_2)
with httpd as server:
    server.serve_forever()
