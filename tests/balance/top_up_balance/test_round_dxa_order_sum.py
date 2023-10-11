import random

import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
from dev_config import AUTH_TOPUP_BALANCE
from utilities.getters import Getters


class TestTopUpBalanceRound:

    """Проверка округления суммы заказа пополнения DXA в долларах"""

    @staticmethod  # создание заказа пополнения баланса
    def top_up_balance_order(auth_token, driver, amount):
        print("Создание заказа на пополнение баланса DXA")
        result = Dexart_api.buy_dxa(auth_token, driver, amount)
        return result

    @staticmethod  # получаем курс DXA
    def get_dxa_rate():
        print("Получение курса DXA")
        result = Dexart_api.dxa_usd_rate()
        Checking.check_status_code(result, 200)
        dxa_rate = Getters.get_json_field_value_2(result, "data", "rate")
        return float(dxa_rate)

    @staticmethod
    def random_amount(a, b):
        random_amount = random.randint(a, b)
        return random_amount

    @staticmethod  # метод округления заказа по математическим правилам до указанного кол-во после запятой (index)
    def round_order_usd_amount(num, index):
        round_num = round(num, index)  # Округляем до двух знаков после запятой
        print(round_num)
        return round_num

    @pytest.mark.parametrize("amount, driver", [
        (random_amount(100, 10000), "oton"),
        (random_amount(15000, 20000), "nearpay"),
        (random_amount(15000, 20000), "transak")
    ])
    def test_top_up_sum_round(self, amount, driver):
        # создаю заказ на покупку DXA
        rate = self.get_dxa_rate()  # получаю курс на момент заказа
        result = self.top_up_balance_order(AUTH_TOPUP_BALANCE, driver=driver, amount=amount)
        Checking.check_status_code(result, 201)
        # получаю проверяемое значение из поля amount
        resul_amount = Getters.get_json_field_value_2(result, "data", "amount")
        # вычисляю ожидаемый результат
        real_usd_amount = amount * rate  # считаю какая будет точная стоимость заказа в usd
        print(f'Реальная сумма заказа в USD будет: {real_usd_amount}')
        expected_usd_amount = self.round_order_usd_amount(real_usd_amount, 2)  # округляю суммую до сотых по мат. правилам
        Checking.assert_values(expected_usd_amount, resul_amount)
