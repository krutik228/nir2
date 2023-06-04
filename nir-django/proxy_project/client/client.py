import requests
import urllib3
import timeit


urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

SSL_CERT_PATH = '/Users/n.krutikov/PycharmProjects/nir-django/venv/lib/python3.9/site-packages/sslserver/certs/development.crt'
ssl_context_sslserver = (
    '/Users/n.krutikov/PycharmProjects/nir-django/venv/lib/python3.9/site-packages/sslserver/certs/development.crt',
    '/Users/n.krutikov/PycharmProjects/nir-django/venv/lib/python3.9/site-packages/sslserver/certs/development.key',
)


def run_time():
    requests.post(
        url='https://localhost:8888/',
        data={
            'firstname': 'Django',
            'secondname': 'Server',
        },
        verify=SSL_CERT_PATH
    )


if __name__ == '__main__':
    times = timeit.repeat(stmt='run_time()', setup="from __main__ import run_time", repeat=10, number=1)
    print(times)