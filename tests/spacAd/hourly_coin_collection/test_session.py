from datetime import datetime, timedelta

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture()
def first_watch():
    def _first_watch(email, signature):
        result = Spacad_api.watch(email, signature)

        watch_time_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        watch_time = datetime.strptime(watch_time_str, "%Y-%m-%d %H:%M:%S")

        coins = Getters.get_json_field_value_2(result, "data", "coins")

        created_at_str = Getters.get_json_field_value_2(result, "data", "created_at")
        created_at = datetime.strptime(created_at_str.replace('T', ' ').replace(".000000Z", ''), "%Y-%m-%d %H:%M:%S")

        expire_at_str = Getters.get_json_field_value_2(result, "data", "expire_at")
        expire_at = datetime.strptime(expire_at_str, "%Y-%m-%d %H:%M:%S")
        return watch_time, created_at, expire_at

    return _first_watch


class TestUserSession:

    """Проверка сессии пользователя"""

    # проверка времени начала сессии
    @pytest.mark.parametrize("email, signature", [(EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)])
    def test_session_create_time(self, set_spacad_ad, check_session, first_watch, email, signature):
        watch_time, created_at, expire_at = first_watch(email, signature)
        print(f'1. {watch_time}')
        print(f'2. {created_at}')
        dif_start_time = watch_time - created_at
        assert timedelta(seconds=0) <= dif_start_time <= timedelta(seconds=2), "Временя не совпало"
        print("Все ок")

    @pytest.mark.parametrize("email, signature", [(EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)])
    def test_session_expire_time(self, set_spacad_ad, first_watch, email, signature):
        watch_time, created_at, expire_at = first_watch(email, signature)
        print(f'1. {created_at}')
        print(f'2. {expire_at}')
        time_dif = expire_at - created_at
        expected_dif = timedelta(minutes=5)
        Checking.assert_values(expected_dif, time_dif)
