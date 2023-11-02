import hashlib
import random
import string

import time

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


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

    @staticmethod
    def check_watch_result(result, status_code, expected):
        Checking.check_status_code(result, status_code)
        actual = Getters.get_json_field_value_0(result, "message")
        expected_result = expected
        Checking.assert_values(expected_result, actual)

    """Проверка подписи по позитивным сценариям"""

    @pytest.mark.parametrize("email, salt, test_name", [
        (EMAIL_SPACAD_WHITELISTED, WEB_SOLT, "Test signature for WEB"),
        (EMAIL_SPACAD_WHITELISTED, ANDROID_SOLT, "Test signature for ANDROID"),
        (EMAIL_SPACAD_WHITELISTED, IOS_SOLT, "Test signature for IOS")])
    def test_signature_watch_ad_positive(self, set_spacad_ad, email, salt, test_name):
        result = Spacad_api.watch(email=email, signature=self.generate_signature(email=email, salt=salt))
        Checking.check_status_code(result, 200)
        expected_fields = ['id', 'coins', 'max_limit', 'min_limit', 'coins_left', 'progress', 'expire_at', 'created_at']
        Checking.check_json_fields_in_v2(result, "data", expected_fields)
        time.sleep(60)  # чтобы можно было собрать следующую монету

    """Проверка подписи по негативным сценариям"""

    @pytest.mark.parametrize("email, salt, expected, test_name", [
        (EMAIL_SPACAD_WHITELISTED, "Wa$ZFkWFGywHx3LsFRPq", "An application update is required", "Test wrong signature"),
        (EMAIL_SPACAD_WHITELISTED, SPACAD_KYC_SIGNATURE, "An application update is required", "Test another user signature"),
        (EMAIL_SPACAD_WHITELISTED, None, "Update application or refresh the page.", "Test no signature")])
    def test_signature_watch_ad_negative(self, set_spacad_ad, email, salt, expected, test_name):
        result = Spacad_api.watch(email=email, signature=self.generate_signature(email=email, salt=salt))
        self.check_watch_result(result, 500, "An application update is required")
        time.sleep(3)