import requests

url = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'


def first_request(jsessionid) -> requests.Response:
    return requests.get(url, cookies={'JSESSIONID': jsessionid})


def post_request(payload, jsessionid) -> requests.Response:
    return requests.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies={'JSESSIONID': jsessionid})
