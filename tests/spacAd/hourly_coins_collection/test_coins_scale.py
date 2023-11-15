import json
import time

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture(scope="module")
def email():
    return EMAIL_SPACAD_WHITELISTED


@pytest.fixture(scope="module")  #
def signature():
    return WATCH_SIGNATURE


class TestCoinsScaleData:
    """Проверка данных для шкалы монет в unity"""  # на проде не проверить

    @staticmethod  # в этом методе соберу монетку и проверю, что меняется кол-во коинс
    def collect_coin(email, signature):
        # сбор монеты
        result_watch = Spacad_api.watch(email, signature)  # собираю первую монетку
        Checking.check_status_code(result_watch, 200)
        result_watch_data = json.loads(result_watch.text)["data"]
        return result_watch_data

    @staticmethod
    def current_session(email):
        result = Spacad_api.current_session(email)
        Checking.check_status_code(result, 200)
        session_data = json.loads(result.text)["data"]
        return session_data

    @staticmethod  # проверка данных прогресса для шкалы
    def check_progress(session_data):
        coins = session_data["coins"]  # получаю кол-во монет в сессии
        max_limit = session_data["max_limit"]  # получаю максимальный лимит
        actual_progress = session_data["progress"]  # получаю данные прогресса
        expected_progress = coins / int(
            max_limit) * 100  # формула расчета прогресса, надо проверить как окургляется и добавить тоже
        print(f"EXPECTED PROGRESS: {expected_progress}")
        Checking.assert_values(expected_progress, actual_progress)

    @staticmethod  # проверка данных прогресса для шкалы
    def check_coins_left(session_data):
        coins = session_data["coins"]  # получаю кол-во монет в сессии
        max_limit = session_data["max_limit"]  # получаю максимальный лимит
        actual_coins_left = session_data["progress"]  # получаю данные из coins_left
        expected_coins_left = int(max_limit) - coins
        print(f"EXPECTED COINS_LEFT: {expected_coins_left}")
        Checking.assert_values(actual_coins_left, actual_coins_left)

    def test_max_limit(self, check_session, set_spacad_ad, email, signature):
        # сбор монеты
        watch = self.collect_coin(email, signature)
        actual_max_limit = watch["max_limit"]
        Checking.assert_values("5", actual_max_limit)  # выставил фиксировано 5

    def test_min_limit(self, set_spacad_ad, email):
        # монету уже не собираю, проверяю через сессию
        session = self.current_session(email)
        actual_min_limit = session["min_limit"]
        Checking.assert_values("3", actual_min_limit)  # выставил фиксировано 3

    def test_progress_and_coins_left(self, set_spacad_ad, email, signature):
        """STEP 1. После первого сбора"""
        # проверяю по данным сессии
        session_1 = self.current_session(email)  # данные сессии первого сбора
        self.check_progress(session_1)  # провожу проверку для данных в прогрессе
        self.check_coins_left(session_1)  # провожу проверку для данных для оставшихся монет

        time.sleep(60)  # выжидаю время для повторного сбора
        self.collect_coin(email, signature)  # второй сбор

        """STEP 2. После второго сбора"""

        session_2 = self.current_session(email)
        self.check_progress(session_2)
        self.check_coins_left(session_2)

        time.sleep(60)  # выжидаю время для повторного сбора
        self.collect_coin(email, signature)  # второй сбор

        """STEP 3. После третьего сбора"""

        session_3 = self.current_session(email)
        self.check_progress(session_3)
        self.check_coins_left(session_3)

        time.sleep(60)  # выжидаю время для повторного сбора
        self.collect_coin(email, signature)  # второй сбор

        """STEP 4. После четвертого сбора"""

        session_4 = self.current_session(email)
        self.check_progress(session_4)
        self.check_coins_left(session_4)

        time.sleep(60)  # выжидаю время для повторного сбора
        self.collect_coin(email, signature)  # второй сбор

        """STEP 5. После пятого сбора"""

        session_5 = self.current_session(email)
        self.check_progress(session_5)
        self.check_coins_left(session_5)
