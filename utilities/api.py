from utilities.http_methods import Http_method
from configuration import DEXART_DEV, COINGLUE_DEV
from src.secrets import API_KEY_DEV
from configuration import MERCHANT_PROD
import json


class Dexart_api:
    """Получение страницы баланса пользователя"""

    @staticmethod
    def user_dxa_balance(auth_token):
        resource = '/api/v1/user/balance'
        url = DEXART_DEV + resource
        print(f'URL: {url}')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """Пополнение баланса DXA"""

    @staticmethod
    def buy_dxa(auth_token, driver, amount):
        resource = '/api/v1/user/balance/top-up'
        url = DEXART_DEV + resource

        payload_top_up = json.dumps({
            "driver": driver,
            "amount": amount
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload_top_up, headers)
        print(f'Response: {result.text}')
        return result

    """Проверка заказа по id заказа"""

    @staticmethod
    def check_order(order_id):
        resource = '/api/v1/user/orders/'
        headers = {'Content-Type': 'application/json'}
        url = DEXART_DEV + resource + str(order_id)
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """Регистрация по нативной рефке"""

    @staticmethod
    def register_dexart_ref(email, ref):
        resource = '/api/v1/auth/register'
        url = DEXART_DEV + resource
        print(f'URL: {url}')

        """Тело запроса"""
        payload = json.dumps({
            "email": email,
            "password": "1qazXSW@",
            "ref": ref
        })
        headers = {
            'x-app-lang': 'en',
            'Content-Type': 'application/json'
        }
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Информация по юзеру"""

    @staticmethod
    def user_referral_info(auth_token):
        resource = '/api/v1/referral/user'
        url = DEXART_DEV + resource

        """Тело запроса"""
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        print(f'All headers: {headers}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Получение курса токена DXA к USD"""

    @staticmethod
    def dxa_usd_rate():
        resource = '/api/v1/dxa/rate'
        url = DEXART_DEV + resource
        print(f'URL: {url}')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': None
        }
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """Создание транзакции пользователю"""

    @staticmethod
    def create_transaction(currency_id, user_id, type_id, status_id, dxa_amount):
        resource = '/api/v1/transactions'
        url = DEXART_DEV + resource
        print(f'URL: {url}')

        """Тело запроса"""
        payload = json.dumps({
            "currency_id": currency_id,
            "user_id": user_id,
            "type_id": type_id,
            "status_id": status_id,
            "amount": dxa_amount,
            "description": "AUTO-TEST",
            "additional": [
                "1",
                "2",
                "3"
            ],
            "is_quiet": False
        })
        headers = {
            'Content-Type': 'application/json',
            'api-key': API_KEY_DEV
        }
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Получении транзакций пользователя (учесть, что есть пагинация)"""

    @staticmethod
    def user_transaction(auth_token):
        resource = '/api/v1/user/transactions'
        url = DEXART_DEV + resource
        print(f'URL: {url}')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        result = Http_method.get(url, headers)
        return result

    """Получение спискай парселей по району"""

    @staticmethod
    def get_region_parcels(region):
        resource = f'/api/v1/maps/districts/{region}/parcels'
        url = DEXART_DEV + resource
        print(f'URL: {url}')
        headers = {}
        result = Http_method.get(url, headers)
        return result

    """Добавление парселя в коризну"""

    @staticmethod
    def add_parcel_to_cart(auth_token, parcel_id):
        resource = '/api/v1/user/cart'
        url = DEXART_DEV + resource

        payload = json.dumps({"parcel_id": parcel_id})
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Добавление парселя в коризну"""

    @staticmethod
    def buy_parcel(auth_token, driver, email):
        resource = '/api/v1/user/cart/buy'
        url = DEXART_DEV + resource

        payload = json.dumps({
            "driver": driver,
            "email": email
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Блок 2FA"""

    """Вывод DXA с баланса"""

    @staticmethod
    def withdraw_dxa(auth_token, amount, code, bsc_address):
        resource = '/api/v1/user/balance/withdrawal'
        url = DEXART_DEV + resource

        payload = json.dumps({
            "amount": amount,
            "code": code,
            "destination": bsc_address
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        # print(f'Response: {result.text}')
        return result

    """блок Gravity Guys"""

    @staticmethod
    def royalties_statistics():
        resource = '/api/v1/app/gravity/statistics'
        url = DEXART_DEV + resource

        payload = {}
        headers = {"api-key": API_KEY_DEV}
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def buy_booster(auth_token, booster_id, amount, room_id):
        resource = '/api/v1/gravity-guys/boosters/set'
        url = DEXART_DEV + resource
        # room_id = Air Test or Pool
        # booster_id = "id": 6 - price 100 DXA, "id": 3 - price 5 DXA
        payload = {'booster_id': booster_id,
                   'amount': amount,
                   'room_uid': room_id}
        headers = {
            'Authorization': f'Bearer {auth_token}'
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def ticket_buy(auth_token, room_id):
        resource = '/api/v1/gravity-guys/records/user-record/buy-tiket'
        url = DEXART_DEV + resource
        # room_id = Air Test or Pool
        # price = 1 DXA
        payload = {'room_uid': room_id}
        headers = {
            'Authorization': f'Bearer {auth_token}'
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def give_royalties():
        resource = '/api/v1/app/give/royalties'
        url = DEXART_DEV + resource
        payload = {}
        headers = {
            'api-key': API_KEY_DEV
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        print("Роялти успешно выданы.")
        return result


class Nft_api:
    """NFT каталог"""

    @staticmethod
    def nft_catalog(param):
        # param - параметр в запросе
        resource = '/api/v1/nft/catalog' + param
        headers = {'Content-Type': 'application/json'}
        url = DEXART_DEV + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def buy_nft(auth_token, nft_id, amount, pay_method):
        resource = '/api/v1/nft/inventory'
        url = DEXART_DEV + resource
        print(f'URL: {url}')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        payload = json.dumps({
            "id": nft_id,
            "source": "web",
            "amount": amount,
            "driver": pay_method
        })
        print(f'Тело запроса = {payload}')
        result = Http_method.post(url, payload, headers)
        #print(f'Response: {result.text}')
        return result

    @staticmethod
    def user_nft_balance(auth_token):
        resource = '/api/v1/nft/inventory'
        url = DEXART_DEV + resource
        print(f'URL: {url}')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        result = Http_method.get(url, headers)
        # print(f'Response: {result.text}')
        return result


class Merchant_api:

    @staticmethod
    def setToken(merchant_id, token):
        resource = "/setToken"
        url = MERCHANT_PROD + resource
        print(f'URL: {url}')

        payload = f'link={merchant_id}&token={token}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        print(f'Тело запроса = {payload}')
        result = Http_method.post(url, payload, headers)
        return result

    # "tokens": {
    #     "USDT": [
    #         {
    #             "id": 1,
    #             "name": "USDT",
    #             "network": "BSC (BEP20)",
    #             "amount": 0.09
    #         },
    #         {
    #             "id": 12,
    #             "name": "USDT",
    #             "network": "Ethereum (ERC20)",
    #             "amount": 0.09
    #         }
    #     ],
    #     "BUSD": [
    #         {
    #             "id": 3,
    #             "name": "BUSD",
    #             "network": "BSC (BEP20)",
    #             "amount": 0.09
    #         }
    #     ],
    #     "BTC": [
    #         {
    #             "id": 8,
    #             "name": "BTC",
    #             "network": "BSC (BEP20)",
    #             "amount": 0.00001001
    #         },
    #         {
    #             "id": 11,
    #             "name": "BTC",
    #             "network": "Bitcoin",
    #             "amount": 0.00001001
    #         }
    #     ],
    #     "DXA": [
    #         {
    #             "id": 10,
    #             "name": "DXA",
    #             "network": "BSC (BEP20)",
    #             "amount": 96
    #         }
    #     ]


class Energy_api:
    """Получение баланса батареек"""

    @staticmethod
    def energy_balance(auth_token):
        resource = f'/api/v1/user/batteries'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        url = DEXART_DEV + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """Активация всех батареек"""

    @staticmethod
    def activate_all_energy(auth_token):
        resource = '/api/v1/user/batteries/activate'
        url = DEXART_DEV + resource

        payload_top_up = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload_top_up, headers)
        print(f'Response: {result.text}')
        return result

    """Активация одной батарейки"""

    @staticmethod
    def activate_one_energy(auth_token, energy_id):
        resource = f'/api/v1/user/batteries/{energy_id}/activate'
        url = DEXART_DEV + resource

        payload_top_up = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload_top_up, headers)
        print(f'Response: {result.text}')
        return result


class Spacad_api:

    """проверка доступа к мероприятию по времени и вайт листу"""

    @staticmethod
    def is_eligible(email):
        resource = f'/api/v1/coinglue/is-eligible?email={email}'
        headers = {'Content-Type': 'application/json'}
        url = COINGLUE_DEV + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result