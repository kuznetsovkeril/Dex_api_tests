import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.utilities import Instruments


@pytest.fixture
def register(ref_id, slug):
    email = Instruments.generate_unique_email()  # генерация уникального email
    result_reg = Dexart_api.register_with_mail(email, ref_id, partner_slug=slug)
    # проверка статус кода
    print(f'Фактический статус код: {result_reg.status_code}')
    Checking.check_status_code(result_reg, 200)
    # получение токена авторизации
    auth_token = Checking.get_json_value(result_reg, "data", "token")
    print(f'Токен авторизации: {auth_token}')
    yield auth_token  # возвращает токен авторизации перед каждым тестом


class TestRegisterRefDexart:
    """Регистрация пользователя в Dexart в разных реф программах"""

    # успешная регистрация в нативной рефке с корректным ref_id, без рефки, под неверной рефкой
    @pytest.mark.parametrize("ref_id, slug, expected_ref_id, test_name", [(789432943, None, 789432943, "Correct referral id"),
                                                                    (1337, None, 1, "Wrong referral id"),
                                                                    (None, None, 1, "No referral id")])
    def test_referral_dexart(self, register, ref_id, slug, expected_ref_id, test_name):
        # Проверка успешной регистрации у нужного рефа
        result_reg_check = Dexart_api.user_referral_info(register)
        Checking.check_json_value_3(result_reg_check, "data", "ref", "id", expected_ref_id)


        # проверка что у дексартовца был создан маркет ид
        # проверка что у пратнера есть поле с партнером
        # проверка что у Атон - что там у Атон?
        # is_created_recently
        # в будущем можно создать файлы и прогнать кейсы регистрации интеграционные (посмотреть в отоне, спакаде и тд)
        # проверить, что при регистрации в Атон также регается в дексарт
