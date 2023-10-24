import hashlib
import random
import string
import json
import time
from datetime import datetime, timedelta

import pytest

from config_check import *
from utilities.api import Spacad_api, Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture()
def set_working_hours():
    # установка расписания
    start_time = datetime.utcnow()  # получаю текущее время utc
    end_time = start_time + timedelta(hours=1)  # прибавляю 1 час для окончания ивента
    # создаю слот расписания
    Spacad_api.set_working_hours(start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"), [])
    # задаю для этого слота settings
    settings = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlaySpacAD"
            }
        ]
    }
    Spacad_api.set_working_hours(start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"), settings)
    print("Расписание установлено")
    yield
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # возвращение предыдущего расписания
    print("Вернул расписание обратно")


class TestWatchSignature:
    """Проверка подписи при отправке события просмотра рекламы"""  # на проде не проверить

    @staticmethod  # генерация подписи
    def generate_signature(email, salt):
        string_elements = string.ascii_letters + string.digits
        random_string = ''.join(random.sample(string_elements, 10))
        random_string_md5 = hashlib.md5(random_string.encode()).hexdigest()
        data = f"{email};{salt};{random_string_md5}"
        signature = hashlib.md5(data.encode()).hexdigest()
        return signature + random_string_md5

    """Проверка подписи по позитивным сценариям"""

    @pytest.mark.parametrize("email, salt, test_name", [
        (EMAIL_SPACAD_WHITELISTED, WEB_SOLT, "Test signature for WEB"),
        (EMAIL_SPACAD_WHITELISTED, ANDROID_SOLT, "Test signature for ANDROID"),
        (EMAIL_SPACAD_WHITELISTED, IOS_SOLT, "Test signature for IOS")])
    def test_signature_watch_ad_positive(self, set_working_hours, email, salt, test_name):
        result = Spacad_api.watch(email=email, signature=self.generate_signature(email=email, salt=salt))
        Checking.check_status_code(result, 200)

        time.sleep(58)  # чтобы можно было собрать следующую монету

    """Проверка подписи по негативным сценариям"""

    @pytest.mark.parametrize("email, salt", [(EMAIL_SPACAD_WHITELISTED, "Wa$ZFkWFGywHx3LsFRPq")])
    def test_wrong_signature_watch_ad(self, set_working_hours, email, salt):
        result = Spacad_api.watch(email=email, signature=self.generate_signature(email=email, salt=salt))
        Checking.check_status_code(result, 500)
        actual = Getters.get_json_field_value_0(result, "message")
        expected = "An application update is required"
        Checking.assert_values(expected, actual)

    @pytest.mark.parametrize("email, salt", [(EMAIL_SPACAD_WHITELISTED, WEB_SOLT)])
    def test_no_signature_watch_ad(self, set_working_hours, email, salt):
        result = Spacad_api.watch(email=EMAIL_SPACAD_WHITELISTED, signature=None)
        Checking.check_status_code(result, 500)
        actual = Getters.get_json_field_value_0(result, "message")
        expected = "Update application or refresh the page."
        Checking.assert_values(expected, actual)
