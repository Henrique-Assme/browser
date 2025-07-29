import socket
import ssl
import string
import sys


class URL:
    def __init__(self, url: string):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            port = int(port)
        self.path = "/" + url

    def request(self):
        request_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )
        request_socket.settimeout(10)
        request_socket.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            request_socket = ctx.wrap_socket(request_socket, server_hostname=self.host)
        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n"
        request += "\r\n"
        request_socket.send(request.encode("utf8"))

        response = request_socket.makefile("r", encoding="utf8", newline="\r\n") # makefile hides the loop needed to collect the bits from the response
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        request_socket.close()
        return content
    
def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url: URL):
    body = url.request()
    show(body)

if __name__ == "__main__":
    load(URL(sys.argv[1]))
    # load(URL("http://example.org/"))