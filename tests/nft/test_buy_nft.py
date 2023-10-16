import pytest

from utilities.api import Nft_api
from utilities.api import Dexart_api
from utilities.checking import Checking
from config_check import *
import time

"""Покупка NFT"""


class Test_buy_nft:
    """Проверка покупки NFT оплатой с баланса"""

    def test_nft_purchase_balance(self):
        print("Buy NFT method")
        # данные в тело запроса
        pay_method = "balance"
        nft_id = 54
        amount = 1
        result = Nft_api.buy_nft(AUTH_DXA_USER, BUY_NFT_ID, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 201)
        # проверка наличия необходимых полей в ответе
        json_fields = ['id', 'driver', 'type', 'status_id', 'amount', 'dxa_amount', 'payment_url', 'paid_at',
                       'created_at']
        Checking.check_json_fields_in_v2(result, "data", json_fields)
        # достаем id созданного заказа
        order_id = Checking.get_json_value(result, "data", "id")
        print(order_id)

        time.sleep(2)  # добавил ожидание, чтобы заказ статус изменился 1 -> 3

        """Проверка статуса заказа"""  # нужно проверить, что после оплаты балансом статус заказа = 3

        result_2 = Dexart_api.check_order(order_id)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result_2, 200)
        Checking.check_json_value_2(result_2, "data", "status_id", 3)

    """Проверка покупки NFT оплатой с криптой"""

    @pytest.mark.prod
    def test_nft_purchase_crypto(self):
        print("Buy NFT method")
        # данные в тело запроса
        pay_method = "oton"
        nft_id = 54
        amount = 1
        result = Nft_api.buy_nft(AUTH_DXA_USER, BUY_NFT_ID, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 201)
        # проверка наличия необходимых полей в ответе
        json_fields = ['id', 'driver', 'type', 'status_id', 'amount', 'dxa_amount', 'payment_url', 'paid_at',
                       'created_at']
        Checking.check_json_fields_in_v2(result, "data", json_fields)
        # проверка на формирование ссылки на оплату
        Checking.check_json_value_searched(result, "data", "payment_url", value_searched="timbi")

    """Проверка покупки NFT оплатой NearPay"""

    @pytest.mark.prod
    def test_nft_purchase_nearpay(self):
        print("Buy NFT method")
        # данные в тело запроса
        pay_method = "nearpay"
        nft_id = 54  # это нфт с ценой 3.5$
        amount = 5
        result = Nft_api.buy_nft(AUTH_DXA_USER, BUY_NFT_ID, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 201)
        # проверка наличия необходимых полей в ответе
        json_fields = ['id', 'driver', 'type', 'status_id', 'amount', 'dxa_amount', 'payment_url', 'paid_at',
                       'created_at']
        Checking.check_json_fields_in_v2(result, "data", json_fields)
        # проверка на формирование ссылки на оплату
        Checking.check_json_value_searched(result, "data", "payment_url", value_searched="nearpay")

    """Проверка покупки NFT оплатой Transak"""

    @pytest.mark.prod
    def test_nft_purchase_transak(self):
        print("Buy NFT method")
        # данные в тело запроса
        pay_method = "transak"
        nft_id = 54
        amount = 5
        result = Nft_api.buy_nft(AUTH_DXA_USER, BUY_NFT_ID, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 201)
        # проверка наличия необходимых полей в ответе
        json_fields = ['id', 'driver', 'type', 'status_id', 'amount', 'dxa_amount', 'payment_url', 'paid_at',
                       'created_at']
        Checking.check_json_fields_in_v2(result, "data", json_fields)
        # проверка на формирование ссылки на оплату
        Checking.check_json_value_searched(result, "data", "payment_url", value_searched="transak")
