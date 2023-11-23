import time
from urllib.parse import urlparse, parse_qs
import pytest

from config_check import *
from pages.office_marketplaces_page import OfficeMarketplacesPage
from utilities.api import Energy_api
from utilities.checking import Checking
from utilities.getters import Getters


class TestBuyEnergyUnits:
    @staticmethod
    def buy_energy_units(auth_token):
        result = Energy_api.buy_energy_units(auth_token)
        Checking.check_status_code(result, 200)
        payment_link = Getters.get_json_field_value_2(result, "data", "link")
        return payment_link

    @staticmethod
    def get_order_id_from_payment_link(url: str):
        parsed_url = urlparse(url)
        order_id_value = parse_qs(parsed_url.query).get('partnerOrderId')
        order_id = str(order_id_value).strip("['']")
        print(order_id)
        return order_id

    def test_oton_accruals_for_energy_units(self):

        # buy EU and get order_id

        payment_link = self.buy_energy_units(AUTH_OTON_USER)
        order_id = self.get_order_id_from_payment_link(payment_link)

        # send callback
        Energy_api.callback_energy_units(order_id=order_id)

        time.sleep(2)
        # check accrual in Oton
        OfficeMarketplacesPage.search_order_in_oton_marketplaces(oton_auth=USER_DEXART_OTON_AUTH, order_id=order_id)


