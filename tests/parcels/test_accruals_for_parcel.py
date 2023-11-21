import json
import time

import pytest

from config_check import *
from utilities.api import Dexart_api, Office_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture()
def buy_parcel(auth_token, price_zone):
    result_parcel_list = Dexart_api.get_region_parcels("REGION-15")  # парсинг списка парселей из 15 района
    Checking.check_status_code(result_parcel_list, 200)
    parcel_id = Getters.get_parcel_by_status(result_parcel_list, status_id=1,
                                             price_zone=price_zone)  # выбирается свободный парсель со статусом 1
    result_add_parcel = Dexart_api.add_parcel_to_cart(auth_token, parcel_id=parcel_id)
    Checking.check_status_code(result_add_parcel, 200)
    print(f"Parcels {parcel_id} added to cart")
    # покупаю этот парсель с баланса для ускорения процесса тестирования
    result_buy_parcel = Dexart_api.buy_parcel(auth_token, driver="balance", email="some_user_email@fexbox.org")
    Checking.check_status_code(result_buy_parcel, 201)
    order_id = Getters.get_json_field_value_2(result_buy_parcel, "data", "id")
    yield order_id
    parcel_return = Dexart_api.return_parcel(parcel_ids=[parcel_id])
    Checking.check_status_code(parcel_return, 200)
    print("Parcel returned in stock")


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

    def test_dexmarket_accruals_for_parcel(self):
        pass