import time

import pytest

from utilities.api import Dexart_api
from utilities.api import Energy_api
from utilities.utilities import Instruments
from utilities.checking import Checking
from dev_config import AUTH_EU_GIFTS
from utilities.getters import Getters


# activates all units before test starts
@pytest.fixture()
def activate_units(auth_token):
    result = Energy_api.activate_all_energy(auth_token)
    Checking.check_status_code(result, 200)
    time.sleep(2)
    print("All EU are activated")


# this fixture buys a parcel and then returns it in stock
@pytest.fixture()
def buy_parcel(auth_token, price_zones):
    for zone in price_zones:
        result_parcel_list = Dexart_api.get_region_parcels("REGION-15")  # парсинг списка парселей из 15 района
        Checking.check_status_code(result_parcel_list, 200)
        parcel_id = Getters.get_parcel_by_status(result_parcel_list, status_id=1,
                                                 price_zone=zone)  # выбирается свободный парсель со статусом 1
        result_add_parcel = Dexart_api.add_parcel_to_cart(auth_token, parcel_id=parcel_id)
        Checking.check_status_code(result_add_parcel, 200)
        print(f"Parcels {parcel_id} added to cart")
    # покупаю этот парсель с баланса для ускорения процесса тестирования
    result_buy_parcel = Dexart_api.buy_parcel(auth_token, driver="balance", email="some_user_email@fexbox.org")
    Checking.check_status_code(result_buy_parcel, 201)
    yield
    user_parcels = Dexart_api.get_user_parcels(auth_token=auth_token)
    parcels_list = Getters.get_user_parcels(user_parcels)
    parcel_return = Dexart_api.return_parcel(parcel_ids=parcels_list)
    Checking.check_status_code(parcel_return, 200)
    print("Parcels are returned in stock")


class TestEnergyGift:
    """Проверка выдачи и объема выданныех EU tokens за покупку парселя"""

    # FAR	25$ - 2 по 10$ и 5 по 1$ = 7 units
    # MEDIUM	45$ - 4 по 10$ и 5 по 1$ = 9 units
    # CENTER	120$ - 12 по 10$ = 12 units

    # FAR	40$ - 4 по 10$ = 4
    # MEDIUM	65$ - 6 по 10$ и 5 по 1$ = 11
    # CENTER	182$ - 18 по 10$ и 2 по 1$ = 20

    # this function returns energy units and tokens balance before land purchase
    @staticmethod
    def energy_balance(auth_token):
        result = Energy_api.energy_balance(auth_token)
        Checking.check_status_code(result, 200)
        inactive_units_balance = Getters.get_json_field_value_4(result, "data", "data", "inactive", "units")
        inactive_units_tokens = Getters.get_json_field_value_4(result, "data", "data", "inactive", "tokens")
        return inactive_units_balance, inactive_units_tokens

    @staticmethod  # получаем курс DXA
    def get_dxa_rate():
        result = Dexart_api.dxa_usd_rate()
        Checking.check_status_code(result, 200)
        dxa_rate = Getters.get_json_field_value_2(result, "data", "rate")
        return float(dxa_rate)

    @staticmethod  # вычисляется ожидаемое кол-во токенов
    def calculate_tokens(usd_amount, dxa_rate):
        tokens_amount = usd_amount / dxa_rate
        print(f'Expected tokens amount: {tokens_amount}')
        return tokens_amount

    @staticmethod  # сравнивается реальное ожидаемое кол-во токенов, с учетом заданного отклонения
    def approximate_tokens_assertion(actual_value, expected_value, tolerance):
        if Instruments.approximately_equal(actual_value, expected_value, tolerance):
            print("Количество токенов сходится с ожиданием.")
        else:
            raise ValueError("Количество токенов НЕ сходится с ожиданием.")

    @pytest.mark.parametrize("auth_token, price_zones, expected_units, usd_amount, test_name", [
        (AUTH_EU_GIFTS, ["LOW"], 7, 25, "Test EU for Low zone parcel"),
        (AUTH_EU_GIFTS, ["MEDIUM"], 9, 45, "Test EU for Medium zone parcel"),
        (AUTH_EU_GIFTS, ["HIGH"], 12, 120, "Test EU for High zone parcel"),
        (AUTH_EU_GIFTS, ["LOW", "MEDIUM", "HIGH"], 28, 190, "Test EU for all zones parcel")])
    def test_gift_eu_parcels(self, activate_units, buy_parcel, auth_token,
                             price_zones, expected_units, usd_amount, test_name):

        # get dxa rate
        dxa_rate = self.get_dxa_rate()

        # waiting to balance updated
        time.sleep(10)

        # check units and tokens amount
        units_balance, tokens_balance = self.energy_balance(auth_token)
        assert units_balance == expected_units, "Wrong gifted Units amount"

        expected_tokens = self.calculate_tokens(usd_amount=usd_amount, dxa_rate=dxa_rate)
        self.approximate_tokens_assertion(actual_value=tokens_balance, expected_value=expected_tokens, tolerance=100)