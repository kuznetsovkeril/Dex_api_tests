import time

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


class TestControlCoinsCollection:

    """Проверка, что между сбором монеты должно быть > 60 секунд"""  # на проде не проверить

    @staticmethod
    def collect_coin():
        # сбор монеты
        result_watch = Spacad_api.watch(EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)
        Checking.check_status_code(result_watch, 200)
        # проверка ответа
        expected_fields = ['id', 'coins', 'max_limit', 'min_limit', 'coins_left', 'progress', 'expire_at', 'created_at']
        Checking.check_json_fields_in_v2(result_watch, "data", expected_fields)

    def test_control_collection(self, set_spacad_ad):
        # первый сбор монеты

        self.collect_coin()

        time.sleep(55)

        # второй сбор монеты - должен быть успех
        self.collect_coin()

        time.sleep(50)

        # третий сбор монеты меньше 55 секунд - должен быть неуспех

        result = Spacad_api.watch(EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)
        Checking.check_json_value(result, "data", False)

        # еще одна попытка собрать монету

        time.sleep(5)
        self.collect_coin()




