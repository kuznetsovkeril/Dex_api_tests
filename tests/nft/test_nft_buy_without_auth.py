import pytest


from utilities.api import Nft_api
from utilities.checking import Checking
from config_check import *
from utilities.getters import Getters


class TestNftBuyWithEmail:

    # The feature was stopped. Users can't buy by only email, they have to auth

    """Проверка покупки NFT с указанием email"""

    @pytest.mark.prod
    @pytest.mark.parametrize("pay_driver, amount, payment_link",
                             [("oton", 1, "timbi"),
                              ("nearpay", 2, "nearpay"),
                              ("transak", 3, "transak")])
    def test_buy_inactive_nft(self, pay_driver, amount, payment_link):

        # данные в тело запроса
        print(f'Покупаемое кол-во NFT: {amount}')
        email = "kirtest@fexbox.org"
        result = Nft_api.buy_nft_with_email(GRAVITY_NFT_ID, amount, pay_driver, email)

        Checking.check_status_code(result, 400)

        message = Getters.get_json_field_value_0(result, "message")
        Checking.assert_values("Inactive product provided", message)

    """Проверка, что неавторизованный юзер не может покупкать с баланса [DEX-3350]"""

    @pytest.mark.prod
    @pytest.mark.parametrize("pay_driver, amount",
                             [("balance", 2)])
    def test_buy_with_email_by_balance(self, pay_driver, amount):

        # данные в тело запроса
        print(f'Покупаемое кол-во NFT: {amount}')
        email = "kirtest@fexbox.org"
        result = Nft_api.buy_nft_with_email(GRAVITY_NFT_ID, amount, pay_driver, email)

        # от полученного статус кода зависит по какой логике будет осуществляться проверка
        Checking.check_status_code(result, 401)
        # если 401, проверяю, что получено нужное сообщение в ответе
        expected_message = "Sign in required to use this payment method"
        Checking.check_json_value(result, "message", expected_message)