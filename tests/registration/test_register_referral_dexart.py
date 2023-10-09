from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.utilities import Instruments

"""Регистрация пользователя по нативной рефке"""


class TestRegisterRefDexart:

    def test_ref_dexart(self):
        print("Register post method")
        email = Instruments.generate_unique_email() #генерация уникального email
        ref_id = 789432943
        print(f'Почта нового юзера: {email}')
        result_reg = Dexart_api.register_dexart_ref(email, ref_id)
        # проверка статус кода
        print(f'Фактический статус код: {result_reg.status_code}')
        Checking.check_status_code(result_reg, 200)
        # проверка наличия поля токен
        Checking.check_one_field_in_json(result_reg, "token")

        """Получение токена авторизации из запроса регистрации"""
        auth_token = Checking.get_json_value(result_reg, "data", "token")
        print(f'Токен авторизации: {auth_token}')

        """Проверка успешной регистрации у нужного рефа"""
        result_reg_check = Dexart_api.user_referral_info(auth_token)
        Checking.check_json_value_3(result_reg_check, "data", "ref", "id", ref_id)

    def test_ref_partner(self):
        pass
        # тут будет кейс регистрации у партнера SpacAd

    def test_ref_client_group(self):
        pass
        # тут будет кейс регистрации в группе клиентов ATON


