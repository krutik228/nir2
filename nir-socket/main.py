import socket
import ssl


CERT_PATH = '/Users/n.krutikov/PycharmProjects/nir-django/cert.pem'
KEY_PATH = '/Users/n.krutikov/PycharmProjects/nir-django/key.pem'

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8443
SERVER_HOST = 'nir-tusur.site'
SERVER_PORT = 443

HEADERS = """\
POST /auth HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""


def get_request_params(request_data: str):
    for row in request_data.split():
        if '=' in row:
            return row.encode()

def add_additional_symbols(param):
    pass


def start_proxy_server(local_host: str, local_port: int) -> None:
    server_context: ssl.SSLContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_context.load_cert_chain(CERT_PATH, KEY_PATH)
    socket_data: bytes = b''
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((LOCAL_HOST, LOCAL_PORT))
            sock.listen(5)
            with server_context.wrap_socket(sock, server_side=True) as ssock:
                while True:
                    print(f"Proxy server started on {local_host}:{local_port}")
                    client_socket, addr = ssock.accept()
                    print(f"Accepted connection from {addr[0]}:{addr[1]}")
                    data: bytes = client_socket.recv(4096)
                    if data:
                        socket_data += data
                        break

        client_context: ssl.SSLContext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        client_context.load_verify_locations(CERT_PATH)
        client_context.check_hostname = False
        server_response: bytes = b''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as server_sock:
            with client_context.wrap_socket(server_sock, server_hostname=SERVER_HOST) as server_ssock:
                server_ssock.connect((SERVER_HOST, SERVER_PORT))
                print(f'Proxy connected to server: {SERVER_HOST}:{SERVER_PORT}')
                params: bytes = get_request_params(socket_data.decode())
                header: bytes = HEADERS.format(
                    content_type="application/x-www-form-urlencoded",
                    content_length=len(params),
                    host=SERVER_HOST + ":" + str(SERVER_PORT)).encode('iso-8859-1')

                payload: bytes = header + params
                server_ssock.send(payload)
                add_additional_symbols(payload)
                while True:
                    data: bytes = server_ssock.recv(4096)
                    if data:
                        server_response += data
                        break
            client_socket.sendall(server_response)
            client_socket.close()
            sock.close()
            ssock.close()
            server_sock.close()
            server_ssock.close()


if __name__ == '__main__':
    # Запуск прокси-сервера
    start_proxy_server(LOCAL_HOST, LOCAL_PORT)
