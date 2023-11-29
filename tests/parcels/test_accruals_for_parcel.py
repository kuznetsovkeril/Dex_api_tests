import time

import pytest

from config_check import *
from pages.dexart_balance_page import DexartBalancePage
from pages.dexart_referral_page import DexartReferralPage
from pages.office_marketplaces_page import OfficeMarketplacesPage
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
        order_id, parcel_id = buy_parcel
        time.sleep(3)
        OfficeMarketplacesPage.search_order_in_partners_marketplaces(base_url=office_url, order_id=order_id)

    """Check accruals for parcel in OTON marketing"""

    @pytest.mark.parametrize("auth_token, price_zone, oton_auth",
                             [(AUTH_OTON_USER, "LOW", USER_DEXART_OTON_AUTH)])
    def test_oton_accruals_for_parcel(self, buy_parcel, auth_token, price_zone, oton_auth):
        order_id, parcel_id = buy_parcel
        time.sleep(3)
        OfficeMarketplacesPage.search_order_in_oton_marketplaces(oton_auth=oton_auth, order_id=order_id)

    """Check accruals for parcel in dexart marketing"""

    @pytest.mark.parametrize("auth_token, price_zone",
                             [(AUTH_DEXART_REF, "LOW")])
    def test_dexmarket_accruals_for_parcel(self, buy_parcel, auth_token, price_zone):
        # get order id
        order_id, parcel_id = buy_parcel
        # check order and get dxa_amount
        dxa_amount = Getters.get_order_dxa_amount(order_id=order_id)
        # get sponsor's ref percent
        ref_percent = DexartReferralPage.get_sponsor_percent(AUTH_DEXART_SPONSOR)
        # check transaction in daxart (time and amount)

        time.sleep(2)

        transaction_amount = DexartBalancePage.get_last_transaction_amount(AUTH_DEXART_SPONSOR)

        # expected amount of ref
        expected_amount = float(dxa_amount) * ref_percent / 100
        print(f'expected: {expected_amount}')

        # assertion
        if Instruments.approximately_equal(expected_amount, transaction_amount, 50):
            pass
        else:
            raise ValueError("Wrong transaction amount!")
