from django.views.decorators.csrf import csrf_exempt
import requests
from typing import Dict
import urllib3
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)


SERVER_URL: str = 'https://nir-tusur.site/'

ADDITIONAL_SYMBOLS = '1:'

HEADERS: Dict = requests.utils.default_headers()
HEADERS.update(
    {
        'User-Agent': 'Mozilla/5.0',
        'From': 'nikkrutik@nail.ru'
    }
)

# Create your views here.
from django.http import HttpResponse


@csrf_exempt
def proxy_view(request):

    name, secondname = request.POST.values()

    data: Dict = {
        'firstname': f'{ADDITIONAL_SYMBOLS} - {name}',
        'secondname': f'{ADDITIONAL_SYMBOLS} - {secondname}',
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
        )
        return HttpResponse(response.text, status=response.status_code)
    except requests.exceptions.RequestException as error:
        raise error
