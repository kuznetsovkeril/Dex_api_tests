import time
import pytest
from utilities.api import Dexart_api
from utilities.utilities import Instruments
from utilities.checking import Checking
from dev_config import AUTH_DXA_WITHDRAW
from src.secrets import USER_SECRET
from utilities.getters import Getters


class TestDxaWithdrawal:
    """Тест вывода DXA с баланса"""
    # В этом кейсе проверяется: вывод работает, баланс изменяется, корректная транзакция создается

    @staticmethod  # получение 2фа кода
    def get_2fa_code(secret):
        code = Instruments.generate_2fa_code(secret)
        return code

    def test_dxa_withdrawal(self):
        # получаем текущий баланс юзера
        result_dxa_balance = Dexart_api.user_dxa_balance(AUTH_DXA_WITHDRAW)
        Checking.check_status_code(result_dxa_balance, 200)
        user_balance = Getters.get_json_field_value_3(result_dxa_balance, "data", "balance", "balance")

        # выводим dxa с баланса
        code = self.get_2fa_code(USER_SECRET)  # получаем 2фа код
        bsc_address = "0xe382b43e5a0deb8aa56c8e07ca82a2492f4c8917"  # любой валидный bsc
        amount = Instruments.random_num(10000, 15999)
        expected_transaction_amount = f'{amount:,.8f}'
        result_withdraw = Dexart_api.withdraw_dxa(AUTH_DXA_WITHDRAW, amount, code, bsc_address)
        # проверка, что не удалось соединиться с сервисом вывода, т.к он не работает на деве
        # сам вывод будет осуществляться корректно
        Checking.check_json_value_searched_1(result_withdraw, "message", "Failed to connect")

        time.sleep(2)  # добавил ожидание, чтобы баланс изменился

        # проверка, что баланс изменился
        expected_balance = float(user_balance) - amount
        print(f'Ожидаемый баланс = {expected_balance}')
        new_result_dxa_balance = Dexart_api.user_dxa_balance(AUTH_DXA_WITHDRAW)
        new_user_balance = Getters.get_json_field_value_3(new_result_dxa_balance, "data", "balance", "balance")
        print(f'Баланс после вывода DXA = {new_user_balance}')
        Checking.assert_values(expected_balance, float(new_user_balance))

        # проверка, что создана транзакция вывода
        # проверка самой транзакции
        user_transactions = Dexart_api.user_transaction(AUTH_DXA_WITHDRAW)
        transaction_amount = Getters.get_object_json_field_value(user_transactions, "data", 0, "amount")
        print(f'В транзакции ожидается сумма: {expected_transaction_amount}')
        Checking.assert_values(expected_transaction_amount, transaction_amount)
        transaction_description = Getters.get_object_json_field_value(user_transactions, "data", 0, "description")
        Checking.assert_values("Withdrawal", transaction_description)
        transaction_status = Getters.get_object_json_field_value_3(user_transactions, "data", 0, "status", "id")
        Checking.assert_values(2, transaction_status)
        transaction_type = Getters.get_object_json_field_value_3(user_transactions, "data", 0, "type", "id")
        Checking.assert_values(5, transaction_type)
        transaction_is_income = Getters.get_object_json_field_value_3(user_transactions, "data", 0, "type", "is_income")
        Checking.assert_values(0, transaction_is_income)
# Кейсы:
#
# 1) успешный вывод AUTH_DXA_WITHDRAW +
#     - баланс изменяется
#     - транзакция есть

# 2) вывод с недостаточным кол-вом средств
# 3) вывод ровно 10к
# 4) вывод меньше 10к
#    4) ввыод нецелого числа
#
# 5) вывод без подключенного 2фа AUTH_WITHOUT_2FA
#     - вывод с неверным 2фа AUTH_DXA_WITHDRAW
# 6) вывод без указания кошелька
# 7) комиссия при выводе (надо получать доступ ко всем транзакция по api)

#
# 8) кейс: неподключен 2фа, потом подключить и снова попробовать вывести
#    9) кейс: подключил 2фа ввел неверный код, потом верный, и потом вывел
