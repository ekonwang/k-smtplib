import socket
import ssl

hostname = 'www.fudan.edu.cn'
context = ssl.create_default_context()
request = 'GET / HTTP/1.1\r\nHost: %s\r\n' %hostname

request = request.encode().replace(b'\n', b'\r\n')
print(request)

sock = socket.create_connection((hostname, 443)) 
ssock = context.wrap_socket(sock, server_hostname=hostname) 
print(ssock.version())
print(ssock.getpeercert())
ssock.send(request)
response = ssock.recv(4096)
print(response.decode('UTF-8'))

