from utilities.http_methods import Http_method
import json

from config_check import *


class Dexart_api:
    """Получение страницы баланса пользователя"""

    @staticmethod
    def user_dxa_balance(auth_token):
        resource = '/api/v1/user/balance'
        url = DEXART + resource
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
        url = DEXART + resource

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

    """Получение информации по юзеру"""

    @staticmethod
    def user_info(auth_token):
        resource = '/api/v1/user'
        url = DEXART + resource
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        # print(f'All headers: {headers}')
        result = Http_method.get(url, headers)
        # print(f'Response: {result.text}')
        return result

    """Проверка заказа по id заказа"""

    @staticmethod
    def check_order(order_id):
        resource = '/api/v1/user/orders/'
        headers = {'Content-Type': 'application/json'}
        url = DEXART + resource + str(order_id)
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """getting all orders"""

    @staticmethod
    def get_orders(auth_token):
        resource = '/api/v1/user/orders/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        url = DEXART + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """Регистрация по рефке"""

    @staticmethod
    def register_with_mail(email, ref, partner_slug):
        resource = '/api/v1/auth/register'
        url = DEXART + resource
        print(f'URL: {url}')

        """Тело запроса"""
        payload = json.dumps({
            "email": email,
            "password": "1qazXSW@",
            "ref": ref,
            "partner": partner_slug
        })
        headers = {
            'x-app-lang': 'en',
            'Content-Type': 'application/json'
        }
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Информация по юзеру в реф программе дексарт"""

    @staticmethod
    def user_referral_info(auth_token):
        resource = '/api/v1/referral/user'
        url = DEXART + resource

        """Тело запроса"""
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        # print(f'All headers: {headers}')
        result = Http_method.post(url, payload, headers)
        # print(f'Response: {result.text}')
        return result

    @staticmethod
    def user_branch(auth_token, email):
        resource = '/api/v1/referral/branch'
        url = DEXART + resource

        """Тело запроса"""
        payload = json.dumps({
            "email": email
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        # print(f'All headers: {headers}')
        result = Http_method.post(url, payload, headers)
        # print(f'Response: {result.text}')
        return result

    """Получение реферального дерева юзера"""

    """Получение курса токена DXA к USD"""

    @staticmethod
    def dxa_usd_rate():
        resource = '/api/v1/dxa/rate'
        url = DEXART + resource
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
        url = DEXART + resource
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
            'api-key': API_KEY
        }
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Получении транзакций пользователя (учесть, что есть пагинация)"""

    @staticmethod
    def user_transaction(auth_token):
        resource = '/api/v1/user/transactions'
        url = DEXART + resource
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
        url = DEXART + resource
        print(f'URL: {url}')
        headers = {}
        result = Http_method.get(url, headers)
        return result

    """Возврат парселя в оборот"""

    @staticmethod
    def return_parcel(parcel_ids):
        resource = '/api/v1/app/parcels/return'
        url = DEXART + resource

        payload = json.dumps({
            "parcels": parcel_ids
        })
        headers = {
            'api-key': API_KEY,
            'Content-Type': 'application/json'
        }

        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Добавление парселя в коризну"""

    @staticmethod
    def add_parcel_to_cart(auth_token, parcel_id):
        resource = '/api/v1/user/cart'
        url = DEXART + resource

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
        url = DEXART + resource

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

    """Получение парселей юзера"""

    @staticmethod
    def get_user_parcels(auth_token):
        resource = '/api/v1/user/parcels'
        url = DEXART + resource
        print(f'URL: {url}')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        result = Http_method.get(url, headers)
        return result

    """Блок 2FA"""

    """Вывод DXA с баланса"""

    @staticmethod
    def withdraw_dxa(auth_token, amount, code, bsc_address):
        resource = '/api/v1/user/balance/withdrawal'
        url = DEXART + resource

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
        url = DEXART + resource

        payload = {}
        headers = {"api-key": API_KEY}
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def buy_booster(auth_token, booster_id, amount, room_id):
        resource = '/api/v1/gravity-guys/boosters/set'
        url = DEXART + resource
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
        url = DEXART + resource
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
        url = DEXART + resource
        payload = {}
        headers = {
            'api-key': API_KEY
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        print("Роялти успешно выданы.")
        return result

    """Gravity Guys methods B2C"""

    @staticmethod  # начало гонки на конкретном уровне гравити гайз
    def start_race(auth_token, room_id):
        resource = '/api/v1/gravity-guys/records/user-record/start-race'
        url = DEXART + resource
        print(f'URL: {url}')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        payload = json.dumps({'room_uid': room_id})
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod  # получение бустеров юзера по типу бустера
    def user_boosters_by_type(auth_token, type_id):
        resource = f'/api/v1/gravity-guys/boosters/by-type?type_id={type_id}'
        url = DEXART + resource
        print(f'URL: {url}')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """Cryptopolia API"""

    # check cryptopolia user

    @staticmethod
    def cryptopolia_user(auth_token):
        resource = f'/api/v1/cryptopolia/user'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        url = DEXART + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result


class Nft_api:
    """NFT каталог"""

    @staticmethod
    def nft_catalog(param):
        # param - параметр в запросе
        resource = '/api/v1/nft/catalog' + param
        headers = {'Content-Type': 'application/json'}
        url = DEXART + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def buy_nft(auth_token, nft_id, amount, pay_method):
        resource = '/api/v1/nft/inventory'
        url = DEXART + resource
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
        # print(f'Response: {result.text}')
        return result

    @staticmethod
    def buy_nft_with_email(nft_id, amount, pay_method, email):
        resource = '/api/v1/nft/inventory'
        url = DEXART + resource
        print(f'URL: {url}')
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({
            "id": nft_id,
            "source": "web",
            "amount": amount,
            "driver": pay_method,
            "email": email
        })
        print(f'Тело запроса = {payload}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def user_nft_balance(auth_token):
        resource = '/api/v1/nft/inventory'
        url = DEXART + resource
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
    def set_token(merchant_id, token):
        resource = "/setToken"
        url = MERCHANT + resource
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
        url = DEXART + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """Активация всех батареек"""

    @staticmethod
    def activate_all_energy(auth_token):
        resource = '/api/v1/user/batteries/activate'
        url = DEXART + resource

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
        url = DEXART + resource

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod  # buy EU
    def buy_energy_units(auth_token):
        resource = f'/api/orders'
        url = ENERGY + resource

        payload = json.dumps({
            "packages": [
                {
                    "id": 1,
                    "count": 1
                }
            ],
            "payment_method": "transak"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + auth_token
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def callback_energy_units(order_id):
        resource = f'/api/orders/callback'
        url = ENERGY + resource

        payload = json.dumps({
            "payment_id": order_id,
            "status": "done",
            "description": "Done manually for test"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result


class Spacad_api:
    """проверка доступа к мероприятию по времени и вайт листу"""

    # проверка на доступ к ивенту
    @staticmethod
    def is_eligible(email):
        resource = f'/api/v1/coinglue/is-eligible?email={email}'
        headers = {'Content-Type': 'application/json'}
        url = COINGLUE + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    # получение расписания ивента
    @staticmethod
    def get_event_schedule():
        resource = f'/api/v1/coinglue/hours/current?all=1'
        headers = {'Content-Type': 'application/json'}
        url = COINGLUE + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        # print(f'Response: {result.text}')
        return result

    # получение активности расписания на текущий момент, если активно - вернет часы, если нет вернет null
    @staticmethod
    def event_open_hours():
        resource = f'/api/v1/coinglue/hours/current'
        headers = {'Content-Type': 'application/json'}
        url = COINGLUE + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result

    """Метод просмотра рекламы (отправка события)"""

    @staticmethod
    def watch(email, signature):
        resource = f'/api/v1/coinglue/watch'
        url = COINGLUE + resource

        payload = json.dumps({
            "email": email,
            "add_id": "1"
        })
        headers = {
            'Signature': signature,
            'Content-Type': 'application/json'
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    """Метод установки респисания рекламы"""

    @staticmethod
    def set_working_hours(start_time, end_time, settings):
        resource = f'/api/v1/coinglue/hours'
        url = COINGLUE + resource

        payload = json.dumps({
            "start": start_time,
            "end": end_time,
            "settings": settings
        })
        headers = {
            'Content-Type': 'application/json',
            'api-key': COINGLUE_API_KEY
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    # удаление расписания

    @staticmethod
    def refresh_working_hours(start_time, end_time):
        resource = f'/api/v1/coinglue/hours/refresh'
        url = COINGLUE + resource

        payload = json.dumps({
            "hours": [
                {
                    "start": start_time,
                    "end": end_time
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'api-key': COINGLUE_API_KEY
        }
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod  # получение текущей сессии пользователя
    def current_session(email):
        resource = f'/api/v1/coinglue/session?email={email}'
        headers = {'Content-Type': 'application/json'}
        url = COINGLUE + resource
        print(f'URL: {url}')
        result = Http_method.get(url, headers)
        print(f'Response: {result.text}')
        return result


"""API различных кабинетов"""


class Office_api:

    @staticmethod
    def list_marketplace(auth):
        resource = f'/transaction/listMarketplace'
        url = OTON + resource

        payload = json.dumps({
            "auth": auth,
            "lang": "en",
            "request": "{\"cmd\":\"get\",\"offset\":0,\"limit\":50,\"sort\":[{\"field\":\"mdate\","
                       "\"direction\":\"desc\"}]"
        })
        print(payload)
        headers = {'Content-Type': 'application/json'}
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        print(f'Response: {result.text}')
        return result

    @staticmethod
    def super_table(base_url, table):
        resource = f'/super/testing/showTable'
        url = base_url + resource

        payload = f'table={table}'
        headers = {'Content-Type': 'application/json'}
        print(f'URL: {url}')
        result = Http_method.post(url, payload, headers)
        # print(f'Response: {result.text}')
        return result
