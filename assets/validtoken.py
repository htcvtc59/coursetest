import requests, json

URL_TARGET_CREATE_TOKEN = 'http://127.0.0.1:8000/api-token-auth/'
URL_TARGET_VALID_TOKEN = 'http://127.0.0.1:8000/api-token-verify/'
URL_TARGET_TOKEN_REFRESH = 'http://127.0.0.1:8000/api-token-refresh/'
USERNAME = 'admin'
PASSWORD = 'admin1234'

headers = {
    "Content-Type": "application/json"
}


def BODYDATAADMIN(USER, PASS):
    data = {
        "username": USER,
        "password": PASS
    }
    return data


def BODYDATATOKEN(TOKEN):
    data = {
        "token": TOKEN
    }
    return data


def validtoken(token):
    content = json.dumps(token)
    res = requests.post(url=URL_TARGET_VALID_TOKEN, data=content, stream=True, headers=headers)
    result = res.json()
    if res.status_code == 200 and result:
        return True
    else:
        return False


def createtoken(username, password):
    content = json.dumps(BODYDATAADMIN(username, password))
    res = requests.post(url=URL_TARGET_CREATE_TOKEN, data=content, stream=True, headers=headers)
    return res.json()
