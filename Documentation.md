## Preface

This browser is written in python because it has an extensive universe of libraries, and a built-in cross-platform UI framework (tkinter).

The initial goal is to understand the algorithms that are used in a browser without carrying to much about handling all errors that a faster and safer language would need, like C/C++/Rust.

I want to actually create this browser in Rust after I finish this first Python version.

## Chapter 1 - Downloading Web Pages

http://example.org/index.html

A URL - uniform resource locator - has three parts:
http - the scheme - it explains hot to get the information
example.org - the host - explains where to get the information
/index.html - the path - explains what information to get

There are also more optional parts to the URl - ports, queries, and fragments

From a URL the browser asks the local OS to put it in touch with the server described by the host name, the OS calls a Domain Name System (DNS) server that converts a host name into a destination IP address.

The OS then decides which hardware will be used to communicate with this IP using a routing table, a table that maps a path to a destination IP.

After connected, the browser requests information from the server using the path. The structure of the request is like this:

GET /index.html HTTP/1.0
Host: example.org

Where GET is the method, /index.html the path, HTTP/1.0 is the HTTP protocol version, Host: is the header and example.org the host value

The browser uses GET when it wants to receive information, then comes the path and finally the HTTP/1.0 which tells the host that the browser speaks version 1.0 of HTTP. There are a lot of HTTP versions, like 1.x, 2.x, 3.x, where each version is way more complex than the version before.

We can test it using the command ```telnet example.org``` followed by the request GET /index.html HTTP/1.0 Host: example.org and a blank line after it, to tell the host that you are done with headers

The response starts with:
HTTP/1.0 200 Ok
That has the HTTP version, the response code (200) and the response description (OK)
Those codes have a lot of meanings, the 100 family are informational messages, 200s mean successful, 300s request follow-up action (ex: redirect), 400s mean sent a bad request and 500s mean the server handled the request badly.

After the 200 Ok, the server sends its own header with a lot of information:
Content-Type: text/html
ETag: "84238dfc8092e5d9c0dac8ef93371a07:1736799080.121134"
Last-Modified: Mon, 13 Jan 2025 20:11:20 GMT
Cache-Control: max-age=2716
Date: Tue, 29 Jul 2025 17:42:23 GMT
Content-Length: 1256
Connection: close
X-N: S

It send about the information requested (content-type, length, last-modified), about the server`(Server, X-Cache), about how long the browser caches this information (Cache-Control, Expires, Etag) and all other stuff. After that it sends the HTML code in the body of the server's response.