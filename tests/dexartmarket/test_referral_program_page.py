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


@pytest.fixture()
def user_branch(auth, email, status_code):
    result = Dexart_api.user_branch(auth, email)
    Checking.check_status_code(result, status_code)
    result_json = json.loads(result.text)
    result_data = result_json["data"]  # получаем json массива data для парсинга всех полей
    yield result_data


class TestDexartReferral:

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
        expected = 0  # ожидается что значение в data для этих юзеров будет False
        Checking.assert_values(expected, data_value)

        print("Реф программа не доступна юзерам вне маркетинга дексарт")

    # проверка наличия нужных полей в ответе ветки реф юзера:
    # юзера в моей ветке 1, 2, 3 уровни, вне моей ветки, самого себя, топа?
    @pytest.mark.parametrize("auth, email, status_code, test_name",
                             [(AUTH_REF_DEXART_1, "testrefka8@fexbox.org", 200, "Test found my level 1 user"),
                              (AUTH_REF_DEXART_1, "testrefka9@fexbox.org", 200, "Test found my level 2 user"),
                              (AUTH_REF_DEXART_1, "refkat18@fexbox.org", 200, "Test found my level 4 user"),
                              (AUTH_REF_DEXART_1, "testrefka@fexbox.org", 200, "Test found my sponsor"),
                              (AUTH_REF_DEXART_1, "disik@mailto.plus", 200, "Test found out of my branch"),
                              (None, "testrefka@fexbox.org", 401, "Test found branch without auth"),
                              (AUTH_REF_DEXART_1, "testrefka.com", 422, "Test found branch with invalid mail"),
                              (AUTH_REF_DEXART_1, " ", 422, "Test found branch with empty mail")])
    def test_user_branch_fields(self, user_branch, auth, email, status_code, test_name):
        current_user_email = user_branch["current_user"]["email"]  #
        print(f'Current user email: {current_user_email}')
        if current_user_email is not False:

            # проверка полей во всем ответе
            data_fields = list(user_branch)
            print(data_fields)
            # expected_fields = ['id', 'email', 'is_assistent', 'account_type', 'referral_link', 'ref', 'ref_count',
            #                    'percent', 'turnover',
            #                    'income', 'ref_income']
            # Checking.assert_values(expected_fields, fields)
            #
            # # проверка наличия нужных полей искомого юзера
            # fields_ref = list(referral_page["data"]["ref"])
            # expected_fields = ['email', 'id', 'account_type']
            # Checking.assert_values(expected_fields, fields_ref)

            # проверка наличия нужных полей у родителей
            branch_fields = list(user_branch["branch"][0])
            print(branch_fields)
            # expected_fields = ['total', 'first_line']
            # Checking.assert_values(expected_fields, fields_ref_count)
            #
            # print("Необходимые поля на странице реф программы присутствуют.")

            # проверка наличия нужных полей
        else:
            print('Юзер не найден в маркетинге Dexart или получена другая ошибка.')
