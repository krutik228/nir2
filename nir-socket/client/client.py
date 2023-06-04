import socket
import ssl
import timeit

# Настройки прокси-сервера
SERVER_HOST = 'nir-tusur.site'
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8443

headers = """\
POST /auth HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""

body = 'firstname=1:John&secondname=1:Week'
body_bytes = body.encode('ascii')
header_bytes = headers.format(
    content_type="application/x-www-form-urlencoded",
    content_length=len(body_bytes),
    host=PROXY_HOST + ":" + str(PROXY_PORT)
).encode('iso-8859-1')
payload = header_bytes + body_bytes


def send_request(host: str, port: int, request: bytes) -> None:
    # PROTOCOL_TLS_CLIENT требуется действительная цепочка сертификатов и имя хоста
    context: ssl.SSLContext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.load_verify_locations('/Users/n.krutikov/PycharmProjects/nir-django/cert.pem')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            ssock.connect((host, port))
            response: bytes = b''
            ssock.send(request)
            while True:
                data: bytes = ssock.recv(4096)
                if data:
                    response += data
                    break
            print(response.decode('UTF-8'))


def run_time():
    send_request(PROXY_HOST, PROXY_PORT, payload)


if __name__ == '__main__':
    # Запрос к прокси-серверу
    times = timeit.repeat(stmt='run_time()', setup="from __main__ import run_time", repeat=10, number=1)
    print(times)

