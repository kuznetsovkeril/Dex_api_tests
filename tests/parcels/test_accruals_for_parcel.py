
import time

import pytest

from config_check import *
from pages.office_marketplaces_page import OfficeMarketplacesPage
from utilities.api import Dexart_api

from utilities.getters import Getters
from utilities.utilities import Instruments


class TestParcelAccruals:

    """Check accruals in partners offices for parcel purchase"""

    @pytest.mark.parametrize("auth_token, price_zone, office_url, test_name",
                             [(AUTH_ATON_USER, "LOW", "https://aton-dev.108dev.ru", "Test accrual for parcel in ATON"),
                              (AUTH_SPACAD_USER, "MEDIUM", "https://spacad-dev.108dev.ru",
                               "Test accrual for parcel in SPACAD"),
                              (AUTH_UP2U_USER_WALLET, "HIGH", "https://up-dev.108dev.ru",
                               "Test accrual for parcel in UP2U")])
    def test_partners_accruals_for_parcel(self, buy_parcel, auth_token, price_zone, office_url, test_name):
        order_id = str(buy_parcel)
        print(order_id)
        time.sleep(5)
        OfficeMarketplacesPage.search_order_in_partners_marketplaces(base_url=office_url, order_id=order_id)

    """Check accruals for parcel in dexart marketing"""

    @pytest.mark.parametrize("auth_token, price_zone",
                             [(AUTH_DEXART_REF, "LOW")])
    def test_dexmarket_accruals_for_parcel(self, buy_parcel, auth_token, price_zone):
        # get order id
        order_id = buy_parcel
        # check order and get dxa_amount
        order_info = Dexart_api.check_order(order_id)
        dxa_amount = Getters.get_json_field_value_2(order_info, "data", "dxa_amount")

        # get sponsor's ref percent
        user_referral_result = Dexart_api.user_referral_info(AUTH_DEXART_SPONSOR)
        ref_percent = Getters.get_json_field_value_2(user_referral_result, "data", "percent")

        # check transaction in daxart (time and amount)
        time.sleep(2)

        user_transactions = Dexart_api.user_transaction(AUTH_DEXART_SPONSOR)
        transaction_amount = Getters.get_object_json_field_value(user_transactions, "data", 0, "amount")
        transaction_amount_float = float(transaction_amount.replace(",", ""))

        # expected amount of ref
        expected_amount = float(dxa_amount) * ref_percent / 100
        print(f'expected: {expected_amount}')

        # assertion
        if Instruments.approximately_equal(expected_amount, transaction_amount_float, 50):
            pass
        else:
            raise ValueError("Wrong transaction amount!")

    """Check accruals for parcel in OTON marketing"""

    @pytest.mark.parametrize("auth_token, price_zone, oton_auth",
                             [(AUTH_OTON_USER, "LOW", USER_DEXART_OTON_AUTH)])
    def test_oton_accruals_for_parcel(self, buy_parcel, auth_token, price_zone, oton_auth):

        order_id = buy_parcel

        time.sleep(3)

        OfficeMarketplacesPage.search_order_in_oton_marketplaces(base_url=OTON, oton_auth=oton_auth, order_id=order_id)
