# кому недоступна реферелка - false
# кому доступна: проверить, что страница отвечает и возвращает нужные поля
import json

import pytest

from config_check import *
from utilities.api import Dexart_api
from utilities.checking import Checking


@pytest.fixture()
def referral_page(auth):
    result = Dexart_api.user_referral_info(auth)
    Checking.check_status_code(result, 200)
    yield json.loads(result.text)


class TestDexartReferralProgram:

    @pytest.mark.parametrize("auth", [AUTH_REF_DEXART])
    def test_referral_page_fields(self, referral_page, auth):
        # проверка полей во всем ответе
        fields = list(referral_page["data"])
        expected_fields = ['id', 'email', 'is_assistent', 'account_type', 'referral_link', 'ref', 'ref_count',
                           'percent', 'turnover',
                           'income', 'ref_income']
        Checking.assert_values(expected_fields, fields)
        # проверка наличия нужных полей спонсора
        fields_ref = list(referral_page["data"]["ref"])
        expected_fields = ['email', 'id', 'account_type']
        Checking.assert_values(expected_fields, fields_ref)
        # проверка наличия нужных полей у кол-ва рефералов
        fields_ref_count = list(referral_page["data"]["ref_count"])
        expected_fields = ['total', 'first_line']
        Checking.assert_values(expected_fields, fields_ref_count)

        print("Необходимые поля на странице реф программы присутствуют.")

    # проверка доступа к реф программе для юзеров из других маркетингов
    @pytest.mark.parametrize("auth", [AUTH_SPACAD_USER, AUTH_OTON_USER, AUTH_GOOGLE_ATON])
    def test_referral_page_for_non_dexart_user(self, referral_page, auth):
        data_value = referral_page["data"]
        print(data_value)
        expected = 0 # ожидается что значение в data для этих юзеров будет False
        Checking.assert_values(expected, data_value)

        print("Реф программа не доступна юзерам вне маркетинга дексарт")
