
import time

import pytest

from config_check import *
from pages.dexart_balance_page import DexartBalancePage
from pages.dexart_referral_page import DexartReferralPage
from pages.office_marketplaces_page import OfficeMarketplacesPage
from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters


# here we check if an order created and purchase successful

class TestProductsAccruals:

    @staticmethod
    def buy_gg_ticket(auth_token, room_id):
        result = Dexart_api.ticket_buy(auth_token=auth_token, room_id=room_id)
        Checking.check_status_code(result, 200)
        order_id = Getters.get_json_field_value_2(result, "data", "id")
        dxa_amount = Getters.get_json_field_value_2(result, "data", "dxa_amount")
        return str(order_id), dxa_amount

    @staticmethod
    def buy_booster(auth_token, booster_id):
        result = Dexart_api.buy_booster(auth_token=auth_token, booster_id=booster_id, amount=1, room_id="Air Test")
        Checking.check_status_code(result, 200)
        order_id = Getters.get_json_field_value_3(result, "data", "order", "id")
        dxa_amount = Getters.get_json_field_value_3(result, "data", "order", "dxa_amount")
        return str(order_id), dxa_amount

    @staticmethod  # получаем курс DXA
    def get_dxa_rate():
        result = Dexart_api.dxa_usd_rate()
        Checking.check_status_code(result, 200)
        dxa_rate = Getters.get_json_field_value_2(result, "data", "rate")
        return float(dxa_rate)

    """Проверка начислений за билет в партнерских кабинетах"""

    @pytest.mark.parametrize("auth_token, office_url, test_name",
                             [(AUTH_ATON_USER, "https://aton-dev.108dev.ru", "Test accrual for gg-ticket in ATON"),
                              (
                                      AUTH_SPACAD_USER, "https://spacad-dev.108dev.ru",
                                      "Test accrual for gg-ticket in SPACAD"),
                              (
                                      AUTH_UP2U_USER_WALLET, "https://up-dev.108dev.ru",
                                      "Test accrual for gg-ticket in UP2U")])
    def test_partners_gg_ticket_accruals(self, auth_token, office_url, test_name):
        order_id, dxa_amount = self.buy_gg_ticket(auth_token, "Air Test")
        time.sleep(3)
        OfficeMarketplacesPage.search_order_in_partners_marketplaces(base_url=office_url, order_id=order_id)

    """Проверка начислений за билет в OTON"""

    def test_oton_gg_ticket_accruals(self):
        order_id, dxa_amount = self.buy_gg_ticket(AUTH_OTON_USER, "Air Test")
        time.sleep(3)
        OfficeMarketplacesPage.search_order_in_oton_marketplaces(base_url=OTON, oton_auth=USER_DEXART_OTON_AUTH, order_id=order_id)

    """Проверка начислений за билет в Dexart"""

    def test_dexart_gg_ticket_accruals(self):
        # buy ticket
        order_id, dxa_amount = self.buy_gg_ticket(AUTH_DEXART_REF, "Air Test")

        # get sponsor's ref percent
        ref_percent = DexartReferralPage.get_sponsor_percent(AUTH_DEXART_SPONSOR)

        # check transaction in daxart (amount)
        time.sleep(2)

        transaction_amount = DexartBalancePage.get_last_transaction_amount(AUTH_DEXART_SPONSOR)

        expected_amount = dxa_amount * ref_percent / 100
        assert expected_amount == float(transaction_amount), "Wrong transaction amount!"

    """Проверка начислений за бустер в партнерских кабинетах"""

    @pytest.mark.parametrize("auth_token, office_url, booster_id, test_name",
                             [(AUTH_ATON_USER, "https://aton-dev.108dev.ru", 6, "Test accrual for booster in ATON"),
                              (AUTH_SPACAD_USER, "https://spacad-dev.108dev.ru", 6,
                               "Test accrual for booster in SPACAD"),
                              (AUTH_UP2U_USER_WALLET, "https://up-dev.108dev.ru", 6,
                               "Test accrual for booster in UP2U")])
    def test_partners_boosters_accruals(self, auth_token, office_url, booster_id, test_name):
        order_id, dxa_amount = self.buy_booster(auth_token, booster_id)

        time.sleep(5)
        OfficeMarketplacesPage.search_order_in_partners_marketplaces(base_url=office_url, order_id=order_id)

    """Проверка начислений за бустер в OTON"""

    def test_oton_booster_accruals(self):

        order_id, dxa_amount = self.buy_booster(auth_token=AUTH_OTON_USER, booster_id=3)
        time.sleep(3)
        OfficeMarketplacesPage.search_order_in_oton_marketplaces(base_url=OTON, oton_auth=USER_DEXART_OTON_AUTH,
                                                                 order_id=order_id)

    """Проверка начислений за бустеры в Dexart"""

    @pytest.mark.parametrize("booster_id, test_name",
                             [(3, "Test booster id 3"),
                              (4, "Test booster id 4"),
                              (5, "Test booster id 5"),
                              (6, "Test booster id 6"),
                              (7, "Test booster id 7"),
                              (8, "Test booster id 8")])
    def test_dexart_gg_booster_accruals(self, booster_id, test_name):
        # https://108dev.myjetbrains.com/youtrack/issue/DEX-3537/Nevernaya-summa-zakaza-usd-pri-pokupke-bustera
        # buy ticket
        order_id, dxa_amount = self.buy_booster(AUTH_DEXART_REF, booster_id)

        # get sponsor's ref percent
        ref_percent = DexartReferralPage.get_sponsor_percent(AUTH_DEXART_SPONSOR)

        # check transaction in daxart (time and amount)
        time.sleep(3)

        # get last transaction amount
        transaction_amount = DexartBalancePage.get_last_transaction_amount(AUTH_DEXART_SPONSOR)

        # assertion
        expected_amount = dxa_amount * ref_percent / 100
        print(expected_amount)
        assert expected_amount == transaction_amount, "Wrong transaction amount!"
