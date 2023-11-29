import json
import time

import pytest

from config_check import *
from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture
def auth_token():
    return AUTH_GG_ORDERS


@pytest.fixture
def buy_gg_ticket(auth_token, room_id):
    result = Dexart_api.ticket_buy(auth_token=auth_token, room_id=room_id)
    Checking.check_status_code(result, 200)
    result_json = json.loads(result.text)
    result_data = result_json["data"]
    yield result_data


@pytest.fixture()
def buy_booster(auth_token, booster_id, amount, room_id):
    result = Dexart_api.buy_booster(auth_token=auth_token, booster_id=booster_id, amount=amount, room_id=room_id)
    Checking.check_status_code(result, 200)
    result_json = json.loads(result.text)
    result_data = result_json["data"]
    yield result_data


@pytest.fixture()
def old_boosters_amount(auth_token, type_id):
    result = Dexart_api.user_boosters_by_type(auth_token, type_id)
    Checking.check_status_code(result, 200)
    booster_amount = Getters.get_json_field_value_0(result, "data")
    yield booster_amount


class TestMarketplaceProducts:

    @staticmethod
    def get_order_data(order_id):
        result = Dexart_api.check_order(order_id=order_id)
        Checking.check_status_code(result, 200)
        result_data = Getters.get_json_field_value_0(result, "data")
        return result_data

    @staticmethod
    def start_race(auth, room):
        result = Dexart_api.start_race(auth_token=auth, room_id=room)
        Checking.check_status_code(result, 200)
        is_have_ticket = Getters.get_json_field_value_2(result, "data", "is_have_tiket")
        return is_have_ticket

    @staticmethod
    def get_user_boosters(auth, type_id):
        result = Dexart_api.user_boosters_by_type(auth, type_id)
        Checking.check_status_code(result, 200)
        booster_amount = Getters.get_json_field_value_0(result, "data")
        return booster_amount

    """Проверка заказа билетов"""

    @pytest.mark.parametrize("room_id, test_name", [
        ("Air Test", "Test create Air Test Ticket order"),
        ("Pool", "Test create Pool Ticket order"),
        ("Fork", "Test create Fork Ticket order")])
    def test_gg_ticket_order(self, buy_gg_ticket, auth_token, room_id, test_name):
        # данные заказа из ответа покупки
        order_id = buy_gg_ticket["id"]
        dxa_amount = buy_gg_ticket["dxa_amount"]

        # данные заказа из ответа проверки заказа
        order = self.get_order_data(order_id=order_id)
        order_dxa_amount = float(order["dxa_amount"])
        assert dxa_amount == order_dxa_amount == 1, "Wrong dxa amount!"

        # проверка, что билеты действительно были куплены и у юзера есть доступ к мероприятию
        time.sleep(2)
        assert self.start_race(auth_token, room_id) == 0, "User doesn't have ticket!"

    """Проверка заказа бустеров"""

    @pytest.mark.parametrize("booster_id, amount, room_id, booster_cost, type_id, uses, test_name",
                             [(3, 1, "Air Test", 5, 1, 10, "Test order booster id 3"),
                              (4, 3, "Pool", 10, 2, 10, "Test order booster id 4"),
                              (5, 2, "Fork", 25, 3, 10, "Test order booster id 5"),
                              (6, 1, "Air Test", 100, 4, 10, "Test order booster id 6"),
                              (7, 1, "Pool", 50, 4, 5, "Test order booster id 7"),
                              (8, 1, "Fork", 10, 4, 2, "Test order booster id 8")])
    def test_booster_order(self, old_boosters_amount, buy_booster, auth_token, booster_id, amount, room_id,
                           booster_cost, type_id, uses, test_name):

        # проверка, что бустеры действительно были куплены и они доступны юзеру
        time.sleep(2)
        assert self.get_user_boosters(auth_token,
                                      type_id) == amount * uses + old_boosters_amount, "Wrong boosters amount!"
