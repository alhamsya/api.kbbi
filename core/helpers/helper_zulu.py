from core.helpers.base import api

HOST = lambda: 'http://api.zulu.id/v1/get-episode'
HEADERS = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache'
}

api_zulu = api(HOST, HEADERS)


def get_the_east(page=1):
    url = '/9/7/0?page={}'.format(page)
    data = api_zulu('get', url)[0]

    if data.get('code') != 200:
        return None

    try:
        result = data['data']['data']
    except (KeyError, ValueError):
        return None
    return result


def get_tonight_show(page=1):
    url = '/9/17/0?page={}'.format(page)
    data = api_zulu('get', url)[0]

    if data.get('code') != 200:
        return None

    try:
        result = data['data']['data']
    except (KeyError, ValueError):
        return None
    return result
