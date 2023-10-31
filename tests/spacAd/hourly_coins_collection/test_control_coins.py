import time

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


class TestControlCoinsCollection:

    """Проверка ограничения 60 сек между монетами и максимума монет за сессию"""  # на проде не проверить

    @staticmethod  # в этом методе соберу монетку и проверю, что меняется кол-во коинс
    def collect_coin(email, signature):
        # сбор монеты
        result_watch = Spacad_api.watch(email, signature)
        Checking.check_status_code(result_watch, 200)
        # проверка ответа
        expected_fields = ['id', 'coins', 'max_limit', 'min_limit', 'coins_left', 'progress', 'expire_at', 'created_at']
        Checking.check_json_fields_in_v2(result_watch, "data", expected_fields)
        coins = Getters.get_json_field_value_2(result_watch, "data", "coins")
        return coins

    @staticmethod
    def failed_collect_coin(email, signature):
        result = Spacad_api.watch(email, signature)
        Checking.check_json_value(result, "data", False)

    @staticmethod
    def get_coins_balance(email):
        result = Spacad_api.current_session(email)
        coins = Getters.get_json_field_value_2(result, "data", "coins")
        return coins

    @staticmethod # проверка, что собрано максимальное кол-во монет в сессии
    def check_max_coins(email):
        result = Spacad_api.current_session(email)
        coins = Getters.get_json_field_value_2(result, "data", "coins")
        max_limit = Getters.get_json_field_value_2(result, "data", "max_limit")
        Checking.assert_values(str(coins), max_limit)

    @pytest.mark.parametrize("email, signature", [(EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)])
    def test_control_collection(self, check_session, set_spacad_ad, email, signature):
        # первый сбор монеты
        self.collect_coin(email, signature)

        # второй сбор через 60 сек
        time.sleep(60)
        self.collect_coin(email, signature)

        # неуспешный сбор через 53 секунды
        time.sleep(53)
        self.failed_collect_coin(email, signature)

        # проверка, что после неуспешного сбора баланс не поменялся в сессии
        session_coins = self.get_coins_balance(email)
        Checking.assert_values(2, session_coins)  # ранее было собрано 2 монетки

        # третий сбор через 7 секунд, суммарно дает >60 сек с предыдущего, поэтому успех
        time.sleep(7)
        self.collect_coin(email, signature)

        # четвертый сбор, больше 60 сек
        time.sleep(61)
        self.collect_coin(email, signature)

        # пятый сбор - тут уже у пользователя в сессии должно быть макс монет за сессии = 5
        time.sleep(58)
        self.collect_coin(email, signature)

        # шестой сбор, который не должен быть успешным, так как сессия еще идет и макс кол-во собрано
        time.sleep(60)
        self.failed_collect_coin(email, signature)

        # проверяю, что у пользователя за сессию собрано макс монет
        self.check_max_coins(email)



