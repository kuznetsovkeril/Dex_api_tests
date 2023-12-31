import pytest

from utilities.api import Nft_api
from utilities.checking import Checking
from config_check import *


class TestNftPurchaseLimit:
    """Проверка лимита оплаты криптой, с баланса и картой"""

    def test_nft_limit_crypto_less(self):  # проверка при оплате криптой менее 2.5$
        print("Buy NFT method")
        pay_method = "oton"
        nft_id = 55  # цена нфт = 1$
        amount = 1
        result = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 422)
        # проверка сообщения в ответе
        expected_message = "The amount of the order by this payment method must be at least 2.5"
        Checking.check_json_value(result, "message", expected_message)

    def test_nft_limit_crypto_sharp(self):  # проверка при оплате криптой суммы ровно 2.5$
        print("Buy NFT method")
        pay_method = "oton"
        nft_id = 56  # цена нфт = 2.5$
        amount = 1
        result = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 201)
        # проверка на верной суммы заказа
        Checking.check_json_value_2(result, "data", "amount", 2.5)
        # проверка на формирование ссылки на оплату
        Checking.check_json_value_searched(result, "data", "payment_url", value_searched="https://timbi.org")

    def test_nft_limit_balance_less(self):  # проверка при оплате с баланса менее 2.5$
        print("Buy NFT method")
        pay_method = "balance"
        nft_id = 55  # цена нфт = 1$
        amount = 1
        result = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 422)
        # проверка сообщения в ответе
        expected_message = "The amount of the order by this payment method must be at least 2.5"
        Checking.check_json_value(result, "message", expected_message)

    def test_nft_limit_balance_sharp(self):  # проверка при оплате балансом суммы ровно 2.5$
        print("Buy NFT method")
        pay_method = "balance"
        nft_id = 56  # цена нфт = 2.5$
        amount = 1
        result = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 201)
        # проверка на формирование ссылки на оплату
        Checking.check_json_value_2(result, "data", "amount", 2.5)

    def test_nft_limit_nearpay_less(self):  # проверка при оплате картой nearpay менее 15$
        print("Buy NFT method")
        pay_method = "nearpay"
        nft_id = 56  # цена нфт = 1$
        amount = 5
        result = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 422)
        # проверка сообщения в ответе
        expected_message = "The amount of the order by this payment method must be at least 15"
        Checking.check_json_value(result, "message", expected_message)

    def test_nft_limit_nearpay_sharp(self):  # проверка при оплате nearpay суммы ровно 15$
        print("Buy NFT method")
        pay_method = "nearpay"
        nft_id = 56  # цена нфт = 2.5$
        amount = 6
        result = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 201)
        # проверка на верной суммы заказа
        Checking.check_json_value_2(result, "data", "amount", 15)
        # проверка на формирование ссылки на оплату
        Checking.check_json_value_searched(result, "data", "payment_url",
                                           value_searched="https://stage-widget.nearpay.co")

    def test_nft_limit_transak_less(self):  # проверка при оплате картой nearpay менее 15$
        print("Buy NFT method")
        pay_method = "transak"
        nft_id = 56  # цена нфт = 1$
        amount = 5
        result = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 422)
        # проверка сообщения в ответе
        expected_message = "The amount of the order by this payment method must be at least 15"
        Checking.check_json_value(result, "message", expected_message)

    def test_nft_limit_transak_sharp(self):  # проверка при оплате transak суммы ровно 15$
        print("Buy NFT method")
        pay_method = "transak"
        nft_id = 56  # цена нфт = 2.5$
        amount = 6
        result = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 201)
        # проверка на верной суммы заказа
        Checking.check_json_value_2(result, "data", "amount", 15)
        # проверка на формирование ссылки на оплату
        Checking.check_json_value_searched(result, "data", "payment_url",
                                           value_searched="https://global-stg.transak.com")

    @pytest.mark.prod
    @pytest.mark.parametrize("pay_method", ["oton", "nearpay", "transak", "balance"])
    def test_nft_purchase_amount(self, pay_method):  # проверить, что кол-во нфт в заказе должно быть не float
        # данные в тело запроса
        amount = 2.5
        result = Nft_api.buy_nft(AUTH_DXA_USER, BUY_NFT_ID, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 422)
        # проверка наличия необходимых полей в ответе
        expected_message = ['The amount must be an integer.']
        Checking.check_json_value_2(result, "errors", "amount", expected_message)

    @pytest.mark.prod
    @pytest.mark.parametrize("pay_method", ["oton", "nearpay", "transak", "balance"])
    def test_nft_purchase_amount_1(self, pay_method):  # проверить, что кол-во нфт в заказе > 0
        # данные в тело запроса
        amount = 0
        result = Nft_api.buy_nft(AUTH_DXA_USER, BUY_NFT_ID, amount, pay_method)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 422)
        # проверка наличия необходимых полей в ответе
        expected_message = ["The amount must be greater than or equal to 1."]
        Checking.check_json_value_2(result, "errors", "amount", expected_message)
