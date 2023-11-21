import json
import time

import pytest

from config_check import *
from utilities.api import Dexart_api, Office_api
from utilities.checking import Checking
from utilities.getters import Getters
from utilities.utilities import Instruments


class TestParcelAccruals:

    @staticmethod
    def search_order_in_marketplace(base_url, order_id):
        result = Office_api.super_table(base_url=base_url, table="marketplace")
        Checking.check_status_code(result, 200)
        # Поиск нужного номера заказа в описании продукта у ATON, SPACAD, UP2U. У OTON такого нет в описании МПЛ
        data = json.loads(result.text)
        for item in data["data"]:
            if order_id in item["product"]:
                print(f'Order id was found in {item}')
                break
        else:
            raise ValueError("Order was not found in marketplaces")

    """Check accruals in partners offices for parcel purchase"""

    @pytest.mark.parametrize("auth_token, price_zone, office_url, test_name",
                             [(AUTH_ATON_USER, "LOW", "https://aton-dev.108dev.ru", "Test accrual for parcel in ATON"),
                              (AUTH_SPACAD_USER, "MEDIUM", "https://spacad-dev.108dev.ru", "Test accrual for parcel in SPACAD"),
                              (AUTH_UP2U_USER_WALLET, "HIGH", "https://up-dev.108dev.ru", "Test accrual for parcel in UP2U")])
    def test_partners_accruals_for_parcel(self, buy_parcel, auth_token, price_zone, office_url, test_name):
        order_id = str(buy_parcel)
        print(order_id)
        time.sleep(5)
        self.search_order_in_marketplace(office_url, order_id=order_id)

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

