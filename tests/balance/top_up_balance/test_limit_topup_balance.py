import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
from dev_config import AUTH_TOPUP_BALANCE


class TestTopUpBalanceLimits:
    """Проверка лимита оплаты криптой, с баланса и картой"""

    @staticmethod
    def top_up_balance_order(auth_token, driver, amount):
        print("Создание заказа на пополнение баланса DXA")
        result = Dexart_api.buy_dxa(auth_token, driver, amount)
        return result

    # проверка при покупке меньше 100 DXA криптой
    @pytest.mark.parametrize("amount, expected_message", [
        (99, "The amount must be greater than or equal to 100."),
        (0, "The amount must be greater than or equal to 100."),
        (None, "The amount field is required.")
    ])
    def test_topup_balance_limit_crypto_less(self, amount, expected_message):
        result = self.top_up_balance_order(AUTH_TOPUP_BALANCE, driver="oton", amount=amount)
        Checking.check_status_code(result, 422)
        # проверка сообщения в ответе
        field_1 = "message"
        Checking.check_json_value(result, field_1, expected_message)

    # проверка меньше лимитов при оплате картой NearPay
    @pytest.mark.parametrize("amount, expected_message", [
        (14999, "The amount must be greater than or equal to 15000."),
        (0, "The amount must be greater than or equal to 15000."),
        (None, "The amount field is required.")
    ])
    def test_topup_balance_limit_nearpay_less(self, amount, expected_message):
        result = self.top_up_balance_order(AUTH_TOPUP_BALANCE, driver="nearpay", amount=amount)
        Checking.check_status_code(result, 422)
        # проверка сообщения в ответе
        field_1 = "message"
        Checking.check_json_value(result, field_1, expected_message)

    # проверка меньше лимитов при оплате картой NearPay
    @pytest.mark.parametrize("amount, expected_message", [
        (14999, "The amount must be greater than or equal to 15000."),
        (0, "The amount must be greater than or equal to 15000."),
        (None, "The amount field is required.")
    ])
    def test_topup_balance_limit_transak_less(self, amount, expected_message):
        result = self.top_up_balance_order(AUTH_TOPUP_BALANCE, driver="transak", amount=amount)
        Checking.check_status_code(result, 422)
        # проверка сообщения в ответе
        field_1 = "message"
        Checking.check_json_value(result, field_1, expected_message)

    # проверка при покупке ровно 15000 DXA через nearpay и transak и 100 DXA криптой
    @pytest.mark.parametrize("amount, card_type, expected_value", [
        (15000, "nearpay", "https://stage-widget.nearpay.co"),
        (15000, "transak", "https://global-stg.transak.com"),
        (100, "oton", "https://timbi.org")
    ])
    def test_topup_balance_limit_cards_sharp(self, amount, card_type, expected_value):
        result = self.top_up_balance_order(AUTH_TOPUP_BALANCE, driver=card_type, amount=amount)
        Checking.check_status_code(result, 201)
        # проверка сообщения в ответе
        Checking.check_json_value_searched(result, "data", "payment_url", value_searched=expected_value)

    # проверка, что пополнить DXA оплатой с баланса нельзя
    def test_topup_balance_from_balance(self):
        result = self.top_up_balance_order(AUTH_TOPUP_BALANCE, driver="balance", amount=15500)
        Checking.check_status_code(result, 422)
        # проверка сообщения в ответе
        field_1 = "message"
        expected_message = "The selected driver is invalid."
        Checking.check_json_value(result, field_1, expected_message)


