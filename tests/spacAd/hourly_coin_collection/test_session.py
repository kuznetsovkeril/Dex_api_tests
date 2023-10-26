import time
from datetime import datetime

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture()
def first_watch(email, signature):
    # первый сбор монетки
    result = Spacad_api.watch(email, signature)
    watch_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    coins = Getters.get_json_field_value_2(result, "data", "coins")
    created_at = Getters.get_json_field_value_2(result, "data", "created_at")
    expire_at = Getters.get_json_field_value_2(result, "data", "expire_at")
    yield watch_time, created_at, expire_at


class TestUserSession:
    """Проверка сессии пользователя"""  # на проде не проверить

    # @staticmethod  # в этом методе соберу монетку и проверю, что меняется кол-во коинс
    # def watch_data(email, signature):
    #     # сбор монеты
    #     result_watch = Spacad_api.watch(email, signature)
    #     Checking.check_status_code(result_watch, 200)
    #     # получение данных
    #     session_id = Getters.get_json_field_value_2(result_watch, "data", "id")
    #     coins = Getters.get_json_field_value_2(result_watch, "data", "coins")
    #     max_limit = Getters.get_json_field_value_2(result_watch, "data", "max_limit")
    #     min_limit = Getters.get_json_field_value_2(result_watch, "data", "min_limit")
    #     coins_left = Getters.get_json_field_value_2(result_watch, "data", "coins_left")
    #     progress = Getters.get_json_field_value_2(result_watch, "data", "progress")
    #     expire_at = Getters.get_json_field_value_2(result_watch, "data", "expire_at")
    #     created_at = Getters.get_json_field_value_2(result_watch, "data", "created_at")
    #     return session_id, coins, max_limit, min_limit, coins_left, progress, expire_at, created_at

    @pytest.mark.parametrize("email, signature", [(EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)])
    def test_session_create_time(self, set_spacad_ad, check_session, first_watch, email, signature):
        watch_time, created_at, expire_at = first_watch
        print(watch_time)
        actual_created_time = created_at.replace('T', ' ').replace(".000000Z", '')
        print(actual_created_time)
        Checking.assert_values(watch_time, actual_created_time)


    # def test_session_expire_time(self, check_session, set_spacad_ad, email, signature):
    #     merchant_link = Getters.get_json_field_value_2(result, "data", "payment_url")
    #     merchant_link_parts = merchant_link.split('/')
    #     merchant_id = merchant_link_parts[-1]


