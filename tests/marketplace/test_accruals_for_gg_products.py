import json
import time

import pytest

from config_check import *
from utilities.api import Dexart_api, Office_api
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

    @staticmethod
    def get_sponsor_percent(auth_token):
        user_referral_result = Dexart_api.user_referral_info(auth_token)
        ref_percent = Getters.get_json_field_value_2(user_referral_result, "data", "percent")
        return ref_percent

    @staticmethod
    def get_transaction_amount(auth_token):
        user_transactions = Dexart_api.user_transaction(auth_token)
        transaction_amount = Getters.get_object_json_field_value(user_transactions, "data", 0, "amount")
        return transaction_amount

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
        time.sleep(5)
        self.search_order_in_marketplace(office_url, order_id=order_id)

    """Проверка начислений за билет в OTON"""

    def test_oton_gg_ticket_accruals(self):
        # price_orig
        # опираться на дату транзакции +- 15 сек?
        pass

    """Проверка начислений за билет в Dexart"""

    def test_dexart_gg_ticket_accruals(self):

        # buy ticket
        order_id, dxa_amount = self.buy_gg_ticket(AUTH_DEXART_REF, "Pool")

        # get sponsor's ref percent
        user_referral_result = Dexart_api.user_referral_info(AUTH_DEXART_SPONSOR)
        ref_percent = Getters.get_json_field_value_2(user_referral_result, "data", "percent")

        # check transaction in daxart (time and amount)
        time.sleep(2)
        user_transactions = Dexart_api.user_transaction(AUTH_DEXART_SPONSOR)
        transaction_amount = Getters.get_object_json_field_value(user_transactions, "data", 0, "amount")

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
        self.search_order_in_marketplace(office_url, order_id=order_id)

    """Проверка начислений за бустер в OTON"""

    def test_oton_booster_accruals(self):
        # price_orig
        # опираться на дату транзакции +- 15 сек?
        pass

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
        ref_percent = self.get_sponsor_percent(AUTH_DEXART_SPONSOR)

        # check transaction in daxart (time and amount)
        time.sleep(3)

        # get transaction amount
        transaction_amount = self.get_transaction_amount(AUTH_DEXART_SPONSOR)
        print(f'TRANSACTION AMOUNT: {transaction_amount}')

        # assertion
        expected_amount = dxa_amount * ref_percent / 100
        print(expected_amount)
        assert expected_amount == float(transaction_amount), "Wrong transaction amount!"
