import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters
from utilities.utilities import Instruments


@pytest.fixture
def register(ref_id, slug):
    email = Instruments.generate_unique_email()  # генерация уникального email
    print(email)
    result_reg = Dexart_api.register_with_mail(email, ref_id, partner_slug=slug)
    # проверка статус кода
    print(f'Фактический статус код: {result_reg.status_code}')
    Checking.check_status_code(result_reg, 200)
    # получение токена авторизации
    auth_token = Checking.get_json_value(result_reg, "data", "token")
    print(f'Токен авторизации: {auth_token}')
    yield auth_token  # возвращает токен авторизации перед каждым тестом


class TestRegisterMarketings:
    """Регистрация пользователя в Dexart в разных реф программах"""

    # успешная регистрация в нативной рефке с корректным ref_id, без рефки, под неверной рефкой
    @pytest.mark.parametrize("ref_id, slug, expected_ref_id, test_name",
                             [(789432943, None, 789432943, "Correct referral id"),
                              (1337, None, 1, "Wrong referral id"),
                              (None, None, 1, "No referral id")])
    def test_reg_in_referral_dexart(self, register, ref_id, slug, expected_ref_id, test_name):
        # Проверка успешной регистрации у нужного рефа в реф программе
        result_user_referral = Dexart_api.user_referral_info(register)
        Checking.check_status_code(result_user_referral, 200)
        Checking.check_json_value_3(result_user_referral, "data", "ref", "id", expected_ref_id)

        # Проверка, что у юзера после регистрации создан market_user_id и он равен id из маркетинга
        result_user_info = Dexart_api.user_info(register)  # в запрос юзер инфо передаем токен из фикстуры
        Checking.check_status_code(result_user_info, 200)
        # получаю market_user_id из user info
        user_market_id = Getters.get_json_field_value_2(result_user_info, "data", "market_user_id")
        # получаю id юзера из реф программы
        ref_user_id = Getters.get_json_field_value_2(result_user_referral, "data", "id")
        # сравниваю эти два поля
        Checking.assert_values(ref_user_id, user_market_id)

    # успешная регистрация в маркетинге партнера
    @pytest.mark.parametrize("ref_id, slug, expected_sponsor_id, test_name",
                             [(1099015389, "spacad", "1099015389", "Correct spacad partner")])
    def test_reg_in_partner_marketing(self, register, ref_id, slug, expected_sponsor_id, test_name):
        result_user_info = Dexart_api.user_info(register)  # в запрос юзер инфо передаем токен из фикстуры
        Checking.check_status_code(result_user_info, 200)
        # получаем и сравниваем slug
        partner_slug = Getters.get_json_field_value_3(result_user_info, "data", "partner", "slug")
        Checking.assert_values("spacad", partner_slug)
        # получаем и сравниваем sponsor_id
        sponsor_id = Getters.get_json_field_value_2(result_user_info, "data", "sponsor_id")
        Checking.assert_values(expected_sponsor_id, sponsor_id)
        # получаю market_user_id и убеждаемся, что он null
        user_market_id = Getters.get_json_field_value_2(result_user_info, "data", "market_user_id")
        Checking.assert_values(None, user_market_id)
