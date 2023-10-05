import time

from utilities.api import Dexart_api
from utilities.api import Merchant_api
from utilities.checking import Checking
from src.auth_tokens import AUTH_TOPUP_BALANCE
from utilities.getters import Getters

"""Top-up balance"""


class Test_top_up_balance:

    def test_top_up_balance(self):
        # получаем текущий баланс юзера
        result_dxa_balance = Dexart_api.user_dxa_balance(AUTH_TOPUP_BALANCE)
        Checking.check_status_code(result_dxa_balance, 200)
        current_dxa_balance = Getters.get_json_field_value_3(result_dxa_balance, "data", "balance", "balance")

        # покупка DXA
        result = Dexart_api.buy_dxa(AUTH_TOPUP_BALANCE, driver="oton", amount=150)  # оплачиваю криптой, так проще
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
        payment_result = Merchant_api.setToken(merchant_id, token=1)  # оплачу в usdt
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
        expected_new_balance = float(current_dxa_balance) + 150.00000000
        Checking.assert_values(float(new_dxa_balance), expected_new_balance)
        print("Баланс успешно пополнился после покупки DXA")
