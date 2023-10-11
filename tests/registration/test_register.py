import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.utilities import Instruments


class TestRegisterRefDexart:
    """Регистрация пользователя в Dexart в разных реф программах"""

    # успешная регистрация в нативной рефке с корректным ref_id, без рефки, под неверной рефкой
    @pytest.mark.parametrize("ref_id, expected_ref_id, test_name", [(789432943, 789432943, "Correct referral id"),
                                                                    (1337, 1, "Wrong referral id"),
                                                                    (None, 1, "No referral id")])
    def test_referral_dexart(self, ref_id, expected_ref_id, test_name):
        print("Register post method")
        email = Instruments.generate_unique_email()  # генерация уникального email
        print(f'Почта нового юзера: {email}')
        result_reg = Dexart_api.register_with_mail(email, ref_id, partner_slug=None)
        # проверка статус кода
        print(f'Фактический статус код: {result_reg.status_code}')
        Checking.check_status_code(result_reg, 200)

        """Получение токена авторизации из запроса регистрации"""
        auth_token = Checking.get_json_value(result_reg, "data", "token")
        print(f'Токен авторизации: {auth_token}')

        """Проверка успешной регистрации у нужного рефа"""
        result_reg_check = Dexart_api.user_referral_info(auth_token)
        expected_sponsor_ref_id = expected_ref_id  # ожидаемое значение после реги в поле реф id в блоке спонсора
        Checking.check_json_value_3(result_reg_check, "data", "ref", "id", expected_ref_id)

    def test_partner_referral(self):
        pass
        # тут будет кейс регистрации у партнера SpacAd, Oton, у которого нет настроек по регистрации

    def test_ref_client_group(self):
        pass

        # проверка что у дексартовца был создан маркет ид
        # проверка что у пратнера есть поле с партнером
        # проверка что у Атон - что там у Атон?
        # is_created_recently
        # в будущем можно создать файлы и прогнать кейсы регистрации интеграционные (посмотреть в отоне, спакаде и тд)
        # проверить, что при регистрации в Атон также регается в дексарт
