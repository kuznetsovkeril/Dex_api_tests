import time

import pytest

from utilities.api import Dexart_api
from utilities.api import Energy_api
from utilities.utilities import Instruments
from utilities.checking import Checking
from dev_config import AUTH_EU_GIFTS
from utilities.getters import Getters


class TestEnergyGift:

    """Проверка выдачи и объема выданныех EU tokens за покупку парселя"""

    # FAR	40$ - 4 по 10$ = 4
    # MEDIUM	65$ - 6 по 10$ и 5 по 1$ = 11
    # CENTER	182$ - 18 по 10$ и 2 по 1$ = 20

    @staticmethod  # получаем баланс неактивных юнитов юзера
    def get_inactive_units_balance(auth_token):
        result = Energy_api.energy_balance(auth_token)
        Checking.check_status_code(result, 200)
        inactive_units_balance = Getters.get_json_field_value_4(result, "data", "data", "inactive", "units")
        return inactive_units_balance

    @staticmethod  # получаем сколько у юзера неактивных токенов
    def get_inactive_tokens_balance(auth_token):
        result = Energy_api.energy_balance(auth_token)
        Checking.check_status_code(result, 200)
        inactive_units_tokens = Getters.get_json_field_value_4(result, "data", "data", "inactive", "tokens")
        return inactive_units_tokens

    @staticmethod  # получаем курс DXA
    def get_dxa_rate():
        result = Dexart_api.dxa_usd_rate()
        Checking.check_status_code(result, 200)
        dxa_rate = Getters.get_json_field_value_2(result, "data", "rate")
        return float(dxa_rate)

    @staticmethod  # выборка перселя из ценовой зоны и добаление в корзину
    def cart_parcel(price_zone, auth_token):
        result_parcel_list = Dexart_api.get_region_parcels("REGION-15")  # парсинг списка парселей из 15 района
        Checking.check_status_code(result_parcel_list, 200)
        parcel_id = Getters.get_parcel_by_status(result_parcel_list, status_id=1,
                                                 price_zone=price_zone)  # выбирается свободный парсель
        print("Добавление нужного парселя(ей) в корзину")
        result_add_parcel = Dexart_api.add_parcel_to_cart(auth_token, parcel_id=parcel_id)
        Checking.check_status_code(result_add_parcel, 200)

    @staticmethod  # покупка добавленых в корзину парселей
    def buy_parcel(auth_token):
        result_buy_parcel = Dexart_api.buy_parcel(auth_token, driver="balance", email="some_user_email@fexbox.org")
        Checking.check_status_code(result_buy_parcel, 201)

    @staticmethod  # активация токенов
    def activate_energy(auth_token):
        result = Energy_api.activate_all_energy(auth_token)
        Checking.check_status_code(result, 200)
        print("Все EU активированы")

    @staticmethod  # вычисляется ожидаемое кол-во токенов
    def calculate_tokens(usd_amount, dxa_rate):
        tokens_amount = usd_amount / dxa_rate
        print(f'Ожидается, прибавилось {tokens_amount} токенов')
        return tokens_amount

    @staticmethod  # сравнивается реальное ожидаемое кол-во токенов, с учетом заданного отклонения
    def approximate_tokens_assertion(real_value, expected_value, tolerance):
        if Instruments.approximately_equal(real_value, expected_value, tolerance):
            print("Количество токенов сходится с ожиданием.")
        else:
            raise ValueError("Количество токенов НЕ сходится с ожиданием.")

    def test_gift_eu_for_low_parcel(self):
        # активация пакетов перед запуском тестов
        self.activate_energy(AUTH_EU_GIFTS)

        time.sleep(2)

        current_units_balance = self.get_inactive_units_balance(AUTH_EU_GIFTS)
        current_tokens_balance = self.get_inactive_tokens_balance(AUTH_EU_GIFTS)
        dxa_rate = self.get_dxa_rate()

        # покупка парселя
        self.cart_parcel("LOW", AUTH_EU_GIFTS)
        time.sleep(1)
        self.buy_parcel(AUTH_EU_GIFTS)

        # добавил ожидание, чтобы баланс успел измениться
        time.sleep(5)

        # проверка количества юнитов
        # добавляю к старому результату 4, так как 40$ - 4 по 10$ - неактуально!!!
        new_units_balance = self.get_inactive_units_balance(AUTH_EU_GIFTS)
        Checking.assert_values(current_units_balance + 7, new_units_balance)

        # проверка количества выданных токенов
        # ожидаемое примерное значение ~ фактическому после получения батареек
        new_tokens_balance = self.get_inactive_tokens_balance(AUTH_EU_GIFTS)
        check_new_tokens_balance = self.calculate_tokens(25, dxa_rate)  # расчет, сколько ожидаю получить на балансе токенов
        expected_new_tokens_balance = current_tokens_balance + check_new_tokens_balance  # ожидаемое изменение на балансе
        print(f'Примерное ожидаемое количество токенов в полученных пакетах = {expected_new_tokens_balance}')
        self.approximate_tokens_assertion(expected_new_tokens_balance, new_tokens_balance, 100)

    def test_gift_eu_for_medium_parcel(self):
        current_units_balance = self.get_inactive_units_balance(AUTH_EU_GIFTS)
        current_tokens_balance = self.get_inactive_tokens_balance(AUTH_EU_GIFTS)
        dxa_rate = self.get_dxa_rate()

        # покупка парселя
        self.cart_parcel("MEDIUM", AUTH_EU_GIFTS)
        time.sleep(1)
        self.buy_parcel(AUTH_EU_GIFTS)

        # добавил ожидание, чтобы баланс успел измениться
        time.sleep(5)

        # проверка количества юнитов
        # добавляю к старому результату 11, так как 65$ - 6 по 10$ и 5 по 1$ = 11
        new_units_balance = self.get_inactive_units_balance(AUTH_EU_GIFTS)
        Checking.assert_values(current_units_balance + 9, new_units_balance)

        # проверка количества выданных токенов
        # ожидаемое примерное значение ~ фактическому после получения батареек
        new_tokens_balance = self.get_inactive_tokens_balance(AUTH_EU_GIFTS)
        check_new_tokens_balance = self.calculate_tokens(45, dxa_rate)  # расчет, сколько ожидаю получить
        expected_new_tokens_balance = current_tokens_balance + check_new_tokens_balance  # ожидаемое изменение на балансе
        print(f'Примерное ожидаемое количество токенов в полученных пакетах = {expected_new_tokens_balance}')
        self.approximate_tokens_assertion(expected_new_tokens_balance, new_tokens_balance, 100)

    def test_gift_eu_for_high_parcel(self):
        current_units_balance = self.get_inactive_units_balance(AUTH_EU_GIFTS)
        current_tokens_balance = self.get_inactive_tokens_balance(AUTH_EU_GIFTS)
        dxa_rate = self.get_dxa_rate()

        # покупка парселя
        self.cart_parcel("HIGH", AUTH_EU_GIFTS)
        time.sleep(1)
        self.buy_parcel(AUTH_EU_GIFTS)

        # добавил ожидание, чтобы баланс успел измениться
        time.sleep(5)

        # проверка количества юнитов
        # добавляю к старому результату 20, так как 182$ - 18 по 10$ и 2 по 1$ = 20
        new_units_balance = self.get_inactive_units_balance(AUTH_EU_GIFTS)
        Checking.assert_values(current_units_balance + 12, new_units_balance)

        # проверка количества выданных токенов
        # ожидаемое примерное значение ~ фактическому после получения батареек
        new_tokens_balance = self.get_inactive_tokens_balance(AUTH_EU_GIFTS)
        check_new_tokens_balance = self.calculate_tokens(120, dxa_rate)  # расчет, сколько ожидаю получить
        expected_new_tokens_balance = current_tokens_balance + check_new_tokens_balance  # ожидаемое изменение на балансе
        print(f'Примерное ожидаемое количество токенов в полученных пакетах = {expected_new_tokens_balance}')
        self.approximate_tokens_assertion(expected_new_tokens_balance, new_tokens_balance, 100)

    def test_gift_eu_for_all_parcels(self, wait_between_tests):  # wait_between - фикстура из конфтеста для ожидания
        # активация пакетов перед запуском тестов
        self.activate_energy(AUTH_EU_GIFTS)
        time.sleep(2)

        current_units_balance = self.get_inactive_units_balance(AUTH_EU_GIFTS)
        current_tokens_balance = self.get_inactive_tokens_balance(AUTH_EU_GIFTS)
        dxa_rate = self.get_dxa_rate()

        # покупка парселя
        price_zones = ["LOW", "MEDIUM", "HIGH"]
        for price_zone in price_zones:
            self.cart_parcel(price_zone, AUTH_EU_GIFTS)
        time.sleep(1)
        self.buy_parcel(AUTH_EU_GIFTS)

        # добавил ожидание, чтобы баланс успел измениться
        time.sleep(5)

        # проверка количества юнитов
        # добавляю к старому результату 35, так как за все 3 зоны дается 35 юнитов
        new_units_balance = self.get_inactive_units_balance(AUTH_EU_GIFTS)
        Checking.assert_values(current_units_balance + 28, new_units_balance)

        # проверка количества выданных токенов
        # ожидаемое примерное значение ~ фактическому после получения батареек
        # номинал всех батареек с трех зон составляет 287$
        new_tokens_balance = self.get_inactive_tokens_balance(AUTH_EU_GIFTS)
        check_new_tokens_balance = self.calculate_tokens(190, dxa_rate)  # расчет, сколько ожидаю получить
        expected_new_tokens_balance = current_tokens_balance + check_new_tokens_balance  # ожидаемое изменение на балансе
        print(f'Примерное ожидаемое количество токенов в полученных пакетах = {expected_new_tokens_balance}')
        self.approximate_tokens_assertion(expected_new_tokens_balance, new_tokens_balance, 100)
