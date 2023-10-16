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
    yield result_json


class TestDexartReferralPage:

    # проверка личной страницы в реф программе
    @pytest.mark.prod
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
    @pytest.mark.prod
    @pytest.mark.parametrize("auth", [AUTH_SPACAD_USER, AUTH_OTON_USER, AUTH_GOOGLE_ATON])
    def test_referral_page_for_non_dexart_user(self, referral_page, auth):
        data_value = referral_page["data"]
        print(data_value)
        expected = 0  # ожидается что значение в data для этих юзеров будет False
        Checking.assert_values(expected, data_value)

        print("Реф программа не доступна юзерам вне маркетинга дексарт")

    # проверка поиска юзера в ветке позитивные сценарии
    @pytest.mark.prod
    @pytest.mark.parametrize("auth, email, status_code, test_name",
                             [(AUTH_REF_DEXART, EMAIL_1ST_LINE, 200, "Test found my level 1 user"),
                              (AUTH_REF_DEXART, EMAIL_2ND_LINE, 200, "Test found my level 2 user"),
                              (AUTH_REF_DEXART, EMAIL_WITHOUT_BRANCH, 200, "Test found user without branch"),
                              (AUTH_REF_DEXART, EMAIL_SPONSOR, 200, "Test found my sponsor"),
                              (AUTH_REF_DEXART, EMAIL_OUT_OF_BRANCH, 200, "Test found out of my branch")])
    def test_search_user_in_branch_positive(self, user_branch, auth, email, status_code, test_name):
        # проверка, что current_user = искомому email
        current_user_email = user_branch["data"]["current_user"]["email"]  # получаем почту из ответа
        print(f'Current user email: {current_user_email}')
        Checking.assert_values(email, current_user_email)

        # проверка наличия необходимых полей в ответе
        data_fields = list(user_branch["data"])
        print(f'Полученные поля: {data_fields}')
        expected_fields = ['current_user', 'branch', 'parents']
        Checking.assert_values(expected_fields, data_fields)

        # проверка полей в блоке искомого юзера
        current_user_fields = list(user_branch["data"]["current_user"])
        print(f'Полученные поля: {current_user_fields}')
        expected_fields = ['user_id', 'email']
        Checking.assert_values(expected_fields, current_user_fields)

    # проверка поиска несуществующего юзера
    @pytest.mark.prod
    @pytest.mark.parametrize("auth, email, status_code, test_name",
                             [(AUTH_REF_DEXART, "nonexistmail@gmail.com", 200, "Test found non-exist user")])
    def test_search_nonexistent_user(self, user_branch, auth, email, status_code, test_name):
        # проверка, что current_user =  False
        current_user_email = user_branch["data"]["current_user"]["email"]  # получаем почту из ответа
        print(f'Current user email: {current_user_email}')
        Checking.assert_values(False, current_user_email)  # проверяем, что он почта = false

    # проверка негативных сценариев поиска рефералов
    @pytest.mark.prod
    @pytest.mark.parametrize("auth, email, status_code, expected_message, test_name",
                             [(" ", EMAIL_2ND_LINE, 401, "Unauthorized", "Test found branch without auth"),
                              (AUTH_REF_DEXART, "testrefka.com", 422, "The email must be a valid email address.",
                               "Test found branch with invalid mail"),
                              (AUTH_REF_DEXART, " ", 422, "The email field is required.",
                               "Test found branch with empty mail")])
    def test_search_user_in_branch_negative(self, user_branch, auth, email, status_code, expected_message, test_name):
        get_message = user_branch["message"]
        print(f'We got message: {get_message}')
        Checking.assert_values(expected_message, get_message)

    # проверка наличия всех поля у юзеров ветки и родителей и юзеров в ветке

    @pytest.mark.prod
    @pytest.mark.parametrize("auth, email, status_code, test_name",
                             [(AUTH_REF_DEXART, EMAIL_1ST_LINE, 200, "Test user with branch")])
    def test_user_branch_fields(self, user_branch, auth, email, status_code, test_name):
        # проверка наличия нужных полей в ветке искомого юзера
        branch_fields = list(user_branch["data"]["branch"][0])
        print(f'Polya: {branch_fields}')
        expected_fields = ['id', 'email', 'level', 'is_assistent', 'percent', 'turnover', 'income', 'ref_income', 'from_percent', 'to_percent', 'ref_count']
        Checking.assert_values(expected_fields, branch_fields)

        # проверка наличия нужных полей у родителей юзера
        parents_fields = list(user_branch["data"]["parents"][0])
        print(f'Поля: {parents_fields}')
        expected_fields = ['id', 'email', 'level', 'is_assistent', 'percent', 'turnover', 'income', 'ref_income',
                           'from_percent', 'to_percent', 'ref_count']
        Checking.assert_values(expected_fields, parents_fields)

    # проверка ответа, если у юзера нет нижестоящих рефералов
    @pytest.mark.prod
    @pytest.mark.parametrize("auth, email, status_code, test_name",
                             [(AUTH_REF_DEXART, EMAIL_WITHOUT_BRANCH, 200, "Test found fields empty branch")])
    def test_user_empty_branch_fields(self, user_branch, auth, email, status_code, test_name):
        # проверка наличия нужных полей в ветке искомого юзера
        branch_fields = list(user_branch["data"]["branch"])
        print(f'Поля: {branch_fields}')
        expected_fields = []
        Checking.assert_values(expected_fields, branch_fields)