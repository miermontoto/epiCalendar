import requests

calendarUrl = 'https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml'
cassiUrl = 'https://cassi.uniovi.es/cas/login?client_name=UnioviAzureAD'

def firstRequest(jsessionid, url=calendarUrl) -> requests.Response:
    return requests.get(url, cookies={'JSESSIONID': jsessionid})

def postRequest(payload, jsessionid, url=calendarUrl) -> requests.Response:
    return requests.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, cookies={'JSESSIONID': jsessionid})
