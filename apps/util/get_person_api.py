import json
from json import JSONDecodeError

import requests


def get_person_api(dni):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token fc062659199a099fade617ceaebfa803308472bb'
    }
    r = requests.get('https://dni.optimizeperu.com/api/prod/persons/' + dni, headers=headers)
    try:
        response_dict = json.loads(r.text)
        return response_dict
    except JSONDecodeError:
        return {"dni": "xxxxx", "name": "xxxxx", "first_name": "xxxxx", "last_name": "xxxxx", "cui": "xxxxx"}


def get_person_api_reniec(dni):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'token 6c5434f660630b32ad09e2f4c525569d5050ab2f'
    }

    try:

        r = requests.get('http://192.168.1.4/api/web-service/person-complete/' + dni, headers=headers,
                         verify=False, stream=True, timeout=10)
        #
        # r = requests.get('http://127.0.0.1:9000/api/web-service/person-basic/' + dni, headers=headers,
        #                  verify=False, stream=True, timeout=10)
        if r.status_code == 200:
            response_dict = json.loads(r.text)
            return response_dict
        else:
            return {"status": "Error", }
    except requests.exceptions.Timeout as e:
        return {"status": "Error", }
