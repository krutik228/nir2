import requests
import ssl
from typing import Dict, Tuple
import timeit

from flask import Flask, request

SERVER_URL: str = 'https://nir-tusur.site/'

ADDITIONAL_SYMBOLS = '1:'

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = True
ssl_context.load_default_certs()
ssl_context.load_verify_locations(
    cafile='/Users/n.krutikov/PycharmProjects/nir-tusur/ssl/my.crt',
    capath=None,
    cadata=None,
)
SSL_CONTEXT: Tuple = (
    '/Users/n.krutikov/PycharmProjects/nir-tusur/ssl/my.crt',
    '/Users/n.krutikov/PycharmProjects/nir-tusur/ssl/my.key'
)


app: Flask = Flask(__name__)

CERT_PATH = '/Users/n.krutikov/PycharmProjects/nir-tusur/ssl/nir.crt'
HEADERS: Dict = requests.utils.default_headers()
HEADERS.update(
    {
        'User-Agent': 'Mozilla/5.0',
        'From': 'nikkrutik@nail.ru'
    }
)
ssl_context_sslserver = (
    '/Users/n.krutikov/PycharmProjects/nir-tusur/ssl/loc.crt',
    '/Users/n.krutikov/PycharmProjects/nir-tusur/ssl/localhost.key',
)


@app.route('/', methods=['POST'])
def proxy() -> requests.Response:
    """
    Прокси сервер.

    Основная задача прокси сервера - приём POST-запроса
    по защищенному SSL соединению,добавление некоторого
    символа к полям запроса с дальнейшим перенаправлением
    запроса на сервер.

    :return: Ответ сервера в виде строки.
    :raise Ошибка при отправке данных.
    """
    # Получение данных из запроса
    data: Dict = {
        'firstname': f'{ADDITIONAL_SYMBOLS} - {request.form.get("firstname")}',
        'secondname': f'{ADDITIONAL_SYMBOLS} - {request.form.get("secondname")}',
    }
    try:
        # Отправка измененных данных на сервер
        response: requests.Response = requests.post(
            # Урл сервера
            url=SERVER_URL,
            # Данные для POST-запроса
            data=data,
            # Заголовки запроса
            headers=HEADERS,
            verify=CERT_PATH
        )
        return response.text
    except requests.exceptions.RequestException as error:
        raise error


if __name__ == '__main__':
    # Точка входа в приложение
    app.run(debug=True, port=8443, ssl_context=ssl_context_sslserver)
