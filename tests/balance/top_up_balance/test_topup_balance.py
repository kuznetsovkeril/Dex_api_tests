import random
import time

import pytest

from utilities.api import Dexart_api
from utilities.api import Merchant_api

from src.auth_tokens import AUTH_TOPUP_BALANCE
from utilities.checking import Checking

from utilities.getters import Getters

"""Top-up balance"""


class TestTopUpBalance:

    @staticmethod  # генерация рандомного чилса в интервале от a и b
    def random_amount(a, b):
        random_amount = random.randint(a, b)
        return random_amount

    @pytest.mark.parametrize("token", [1, 10])   # также проверяется попытка пополнить за DXA [DEX-3379]
    def test_top_up_balance(self, token):
        # получаем текущий баланс юзера
        result_dxa_balance = Dexart_api.user_dxa_balance(AUTH_TOPUP_BALANCE)
        Checking.check_status_code(result_dxa_balance, 200)
        current_dxa_balance = Getters.get_json_field_value_3(result_dxa_balance, "data", "balance", "balance")

        # покупка DXA
        amount = self.random_amount(100, 10000)  # генерирую рандомное число
        expected_transaction_amount = f'{amount:,.8f}'
        result = Dexart_api.buy_dxa(AUTH_TOPUP_BALANCE, driver="oton", amount=amount)  # оплачиваю криптой, так проще
        Checking.check_status_code(result, 201)

        # проеряем, что id заказа = 1 и еще не оплачен
        Checking.check_json_value_2(result, "data", "status_id", 1)

        # получаем id заказа в системе Dexart
        order_id = Getters.get_json_field_value_2(result, "data", "id")

        # получаем id мерчанта для оплаты заказа
        merchant_link = Getters.get_json_field_value_2(result, "data", "payment_url")
        merchant_link_parts = merchant_link.split('/')
        merchant_id = merchant_link_parts[-1]
        print(merchant_id)

        # оплачиваем заказ
        payment_result = Merchant_api.set_token(merchant_id, token=token)  # оплачу в usdt
        print(f"Token_id = {token}")
        Checking.check_status_code(result, 201)

        print("Ожидание 40 секунд для проведения оплаты в мерчанте")
        time.sleep(40)

        # проверка, что статус заказа изменился на "оплачено" 1 -> 3
        new_order_result = Dexart_api.check_order(order_id)
        Checking.check_status_code(new_order_result, 200)
        check_order_id = Getters.get_json_field_value_2(result, "data", "id")
        Checking.check_json_value_2(new_order_result, "data", "status_id", 3)

        # проверка, что после покупке DXA баланс изменился
        result_new_dxa_balance = Dexart_api.user_dxa_balance(AUTH_TOPUP_BALANCE)
        Checking.check_status_code(result_new_dxa_balance, 200)
        new_dxa_balance = Getters.get_json_field_value_3(result_new_dxa_balance, "data", "balance", "balance")
        expected_new_balance = float(current_dxa_balance) + amount
        Checking.assert_values(float(new_dxa_balance), expected_new_balance)
        print("Баланс успешно пополнился после покупки DXA")

        # проверка транзакции пополнения баланса у пользователя
        user_transactions = Dexart_api.user_transaction(AUTH_TOPUP_BALANCE)
        transaction_amount = Getters.get_object_json_field_value(user_transactions, "data", 0, "amount")
        print(f'В транзакции ожидается сумма: {expected_transaction_amount}')
        Checking.assert_values(expected_transaction_amount, transaction_amount)
        transaction_description = Getters.get_object_json_field_value(user_transactions, "data", 0, "description")
        Checking.assert_values("Balance top-up", transaction_description)
        transaction_status = Getters.get_object_json_field_value_3(user_transactions, "data", 0, "status", "id")
        Checking.assert_values(2, transaction_status)
        transaction_type = Getters.get_object_json_field_value_3(user_transactions, "data", 0, "type", "id")
        Checking.assert_values(7, transaction_type)
        transaction_is_income = Getters.get_object_json_field_value_3(user_transactions, "data", 0, "type", "is_income")
        Checking.assert_values(1, transaction_is_income)
