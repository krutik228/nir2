import requests
import logging
import timeit


headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
        'From': 'nikkrutik@nail.ru'
    }
)

PROXY_URL = 'https://127.0.0.1:8443'
CERT_PATH = '/Users/n.krutikov/PycharmProjects/nir-tusur/ssl/loc.crt'


def send_request() -> requests.Response:
    """
    Отправка запроса на сервер через прокси.

    Отправляет POST запрос по защищенному соединению на прокси с
    помощью request запроса с указанными параметрами хедера.

    :return: Ответ сервера.
    """
    resp: requests.Response = requests.post(
        url=PROXY_URL,
        data={
            'firstname': 'Dadaya',
            'secondname': 'Sedmoy'
        },
        verify=CERT_PATH,
        headers=headers,
    )
    return resp


if __name__ == '__main__':
    time_sum = timeit.repeat(stmt='send_request()', setup="from __main__ import send_request", repeat=10, number=1)
    print(time_sum)
