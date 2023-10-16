import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters
from config_check import *


class Test_user_dxa_balance:

    @pytest.mark.prod
    def test_show_user_balance(self):
        result = Dexart_api.user_dxa_balance(auth_token=AUTH_BALANCE_PAGE_USER)
        Checking.check_status_code(result, 200)
        # проверка наличия необходимых полей баланса

        # 1) проверка полей основного баланса
        balance_fields = Checking.show_all_fields(result, "data", "balance")
        expected_fields = ['currency', 'balance', 'balance_usd']
        Checking.assert_values(balance_fields, expected_fields)
        print("Необходимые поля в блоке баланса присутствуют")

        # 2) проверка названий статей дохода
        for index in range(6):
            income_item_name = Getters.get_json_field_value(result, "data", "income", index, "name")
            print(income_item_name)
            expected_name = (
                "Energy Units", "Events", "Gravity NFT royalties", "Referral reward", "Staking income", "Other")
            assert income_item_name in expected_name, f"Название '{income_item_name}' не соответствует ожиданиям у юзера {AUTH_BALANCE_PAGE_USER}."
            print(f"Проверка для названия '{income_item_name}' выполнена.")

        # 3) проверка статей расхода
        for index in range(4):
            expense_item_name = Getters.get_json_field_value(result, "data", "expenses", index, "name")
            print(expense_item_name)
            expected_name = ("Shopping", "Staking", "Withdrawal", "Other")
            assert expense_item_name in expected_name, f"Название '{expense_item_name}' не соответствует ожиданияму юзера {AUTH_BALANCE_PAGE_USER}."
            print(f"Проверка для названия '{expense_item_name}' выполнена.")

    # проверка, что курс подтягивается для баланса USD и баланс usd считает верно

    @pytest.mark.prod
    def test_usd_balance(self):

        # проверка, что курс приходит и он больше нуля

        result_rate = Dexart_api.dxa_usd_rate()
        Checking.check_status_code(result_rate, 200)
        # получаем текущее значение курса
        dxa_rate = Checking.get_json_value(result_rate, "data", "rate")
        assert float(dxa_rate) > 0, "Ошибка в курсе"
        print("Курс dxa успешно получен")

        # проверка, что при расчете баланса USD используется курс USD/DXA
        # проверка округления баланса USD до сотых по математическим правилам

        result_balance = Dexart_api.user_dxa_balance(auth_token=AUTH_BALANCE_PAGE_USER)
        Checking.check_status_code(result_balance, 200)
        dxa_balance = Getters.get_json_field_value_3(result_balance, "data", "balance", "balance")
        real_usd_balance = Getters.get_json_field_value_3(result_balance, "data", "balance", "balance_usd")
        check_usd_balance = float(dxa_balance) * float(dxa_rate)
        expected_usd_balance = round(check_usd_balance, 2)
        print(f'Ожидаемый баланс после округления = {expected_usd_balance}')
        Checking.assert_values(expected_usd_balance, float(real_usd_balance))
        print("Баланс USD пошел проверку")

    # проверка, что у юзеров вне маркетингов дексарт нет статьи дохода реферальная программа, а остальные есть

    @pytest.mark.prod
    def test_non_dexart_users(self):
        users = [AUTH_OTON_USER, AUTH_GOOGLE_ATON, AUTH_SPACAD_USER]
        for user in users:
            result = Dexart_api.user_dxa_balance(auth_token=user)
            Checking.check_status_code(result, 200)
            print(user)
            balance_fields = Checking.show_all_fields(result, "data", "balance")
            expected_fields = ['currency', 'balance', 'balance_usd']
            Checking.assert_values(balance_fields, expected_fields)
            print("Необходимые поля в блоке баланса присутствуют")

            # 2) проверка названий статей дохода
            for index in range(5):
                income_item_name = Getters.get_json_field_value(result, "data", "income", index, "name")
                print(income_item_name)
                expected_name = ("Energy Units", "Events", "Gravity NFT royalties", "Staking income", "Other")
                assert income_item_name in expected_name, f"Название '{income_item_name}' не соответствует ожиданиям у юзера {user}."
                print(f"Проверка для названия '{income_item_name}' выполнена.")

            # 3) проверка статей расхода

            for index in range(4):
                expense_item_name = Getters.get_json_field_value(result, "data", "expenses", index, "name")
                print(expense_item_name)
                expected_name = ("Shopping", "Staking", "Withdrawal", "Other")
                assert expense_item_name in expected_name, f"Название '{expense_item_name}' не соответствует ожиданиям у юзера {user}."
                print(f"Проверка для названия '{expense_item_name}' выполнена.")
