import requests

"""Http methods"""


class Http_method:
    headers = {'Content-Type': 'application/json'}
    cookies = None


    @staticmethod
    def get(url, headers):
        result = requests.get(url, headers=headers, cookies=Http_method.cookies)
        return result

    @staticmethod
    def post(url, payload, headers):
        result = requests.post(url, data=payload, headers=headers, cookies=Http_method.cookies)
        return result

    @staticmethod
    def delete(url, payload):
        result = requests.delete(url, data=payload, headers=Http_method.headers, cookies=Http_method.cookies)
        return result

    @staticmethod
    def put(url, payload):
        result = requests.delete(url, data=payload, headers=Http_method.headers, cookies=Http_method.cookies)
        return result
