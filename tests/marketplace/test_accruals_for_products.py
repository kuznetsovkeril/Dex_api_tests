import json
import time

import pytest

from config_check import *
from utilities.api import Dexart_api, Office_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture
def auth():
    return OTON_DEXART_USER


class TestProductsAccruals:

    @staticmethod
    def buy_gg_ticket(auth_token, room_id):
        result = Dexart_api.ticket_buy(auth_token=auth_token, room_id=room_id)
        Checking.check_status_code(result, 200)
        order_id = Getters.get_json_field_value_2(result, "data", "id")
        return str(order_id)

    @staticmethod
    def buy_booster(auth_token, booster_id):
        result = Dexart_api.buy_booster(auth_token=auth_token, booster_id=booster_id, amount=1, room_id="Air Test")
        Checking.check_status_code(result, 200)
        order_id = Getters.get_json_field_value_3(result, "data", "order", "id")
        return str(order_id)

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

    """Проверка начислений за билет в партнерских кабинетах"""

    @pytest.mark.parametrize("auth_token, office_url, test_name",
                             [(AUTH_ATON_USER, "https://aton-dev.108dev.ru", "Test accrual for gg-ticket in ATON"),
                              (
                              AUTH_SPACAD_USER, "https://spacad-dev.108dev.ru", "Test accrual for gg-ticket in SPACAD"),
                              (AUTH_UP2U_USER, "https://up-dev.108dev.ru", "Test accrual for gg-ticket in UP2U")])
    def test_partners_gg_ticket_accruals(self, auth_token, office_url, test_name):
        order_id = self.buy_gg_ticket(auth_token, "Air Test")
        time.sleep(5)
        self.search_order_in_marketplace(office_url, order_id=order_id)

    """Проверка начислений за билет в OTON"""

    def test_oton_gg_ticket_accruals(self):
        # price_orig
        # опираться на дату транзакции +- 15 сек?
        pass

    """Проверка начислений за бустер в партнерских кабинетах"""

    @pytest.mark.parametrize("auth_token, office_url, booster_id, test_name",
                             [(AUTH_ATON_USER, "https://aton-dev.108dev.ru", 6, "Test accrual for booster in ATON"),
                              (AUTH_SPACAD_USER, "https://spacad-dev.108dev.ru", 6,
                               "Test accrual for booster in SPACAD"),
                              (AUTH_UP2U_USER, "https://up-dev.108dev.ru", 6, "Test accrual for booster in UP2U")])
    def test_partners_boosters_accruals(self, auth_token, office_url, booster_id, test_name):
        order_id = str(self.buy_booster(auth_token, booster_id))
        time.sleep(5)
        self.search_order_in_marketplace(office_url, order_id=order_id)
