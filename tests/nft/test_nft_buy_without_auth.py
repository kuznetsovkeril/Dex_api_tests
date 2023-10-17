import pytest


from utilities.api import Nft_api
from utilities.checking import Checking
from config_check import *


class TestNftBuyWithEmail:

    """Проверка покупки NFT с указанием email"""

    @pytest.mark.prod
    @pytest.mark.parametrize("pay_driver, amount, payment_link",
                             [("oton", 1, "timbi"),
                              ("nearpay", 3, "nearpay"),
                              ("transak", 4, "transak")])
    def test_buy_nft_with_email(self, pay_driver, amount, payment_link):

        # данные в тело запроса
        print(f'Покупаемое кол-во NFT: {amount}')
        email = "kirtest@fexbox.org"
        result = Nft_api.buy_nft_with_email(GRAVITY_NFT_ID, amount, pay_driver, email)

        # от полученного статус кода зависит по какой логике будет осуществляться проверка
        Checking.check_status_code(result, 201)
        # если 201, проверяю, что создана ссылка для оплаты
        value_searched = payment_link  # буду проверять, по части ссылок на оплату oton, transak, nearpay
        Checking.check_json_value_searched(result, "data", "payment_url", value_searched)

    """Проверка, что неавторизованный юзер не может покупкать с баланса [DEX-3350]"""

    @pytest.mark.prod
    @pytest.mark.parametrize("pay_driver, amount, payment_link",
                             [("balance", 2, None)])
    def test_buy_with_email_by_balance(self, pay_driver, amount, payment_link):

        # данные в тело запроса
        print(f'Покупаемое кол-во NFT: {amount}')
        email = "kirtest@fexbox.org"
        result = Nft_api.buy_nft_with_email(GRAVITY_NFT_ID, amount, pay_driver, email)

        # от полученного статус кода зависит по какой логике будет осуществляться проверка
        Checking.check_status_code(result, 401)
        # если 401, проверяю, что получено нужное сообщение в ответе
        expected_message = "Sign in required to use this payment method"
        Checking.check_json_value(result, "message", expected_message)
