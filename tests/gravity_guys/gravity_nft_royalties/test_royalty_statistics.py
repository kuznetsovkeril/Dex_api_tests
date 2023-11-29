import time

import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking

from dev_config import AUTH_BUY_GG_ITEMS
from utilities.getters import Getters


class TestRoyaltyStatistics:
    """Проверка статистики для раздачи Royalties"""

    # запуск раздачи royalties
    @staticmethod
    def give_royalties():
        result = Dexart_api.give_royalties()
        Checking.check_status_code(result, 200)
        print("Все роялти выданы пользователям")

    @staticmethod
    def buy_ticket(room_id):
        result_buy_ticket = Dexart_api.ticket_buy(AUTH_BUY_GG_ITEMS, room_id=room_id)
        print(f'Room ID: {room_id}')
        Checking.check_status_code(result_buy_ticket, 200)

    # метод покупки booster
    @staticmethod
    def buy_booster(booster_id, room_id):
        result_buy_booster = Dexart_api.buy_booster(AUTH_BUY_GG_ITEMS, booster_id=booster_id, amount=1, room_id=room_id)
        print(f'Room ID: {room_id}')
        Checking.check_status_code(result_buy_booster, 200)
        print("Бустер успешно куплен")

    @staticmethod
    def refresh_statistic():
        result = Dexart_api.royalties_statistics()
        Checking.check_status_code(result, 200)
        fund_value = Getters.get_json_field_value_0(result, "fund")
        fund_acc_value = Getters.get_json_field_value_0(result, "fund_acc")
        royalty_value = Getters.get_json_field_value_0(result, "royalty")
        print("Статистика получена и обновлена")
        return fund_value, fund_acc_value, royalty_value

    @staticmethod
    def assert_fund_income(old_fund_value, old_fund_acc_value, expected_income):
        result = Dexart_api.royalties_statistics()  # получу обновленную статистику
        new_fund_value = Getters.get_json_field_value_0(result, "fund")
        new_fund_acc_value = Getters.get_json_field_value_0(result, "fund_acc")
        expected_fund_income = old_fund_value + expected_income
        print(f'Ожидаемое новое fund_income = {expected_fund_income}')
        Checking.assert_values(expected_fund_income, new_fund_value)
        expected_fund_acc_income = old_fund_acc_value + expected_income
        print(f'Ожидаемое новое fund_acc_income = {expected_fund_acc_income}')
        Checking.assert_values(expected_fund_acc_income, new_fund_acc_value)

    # проверка, что все виды покупок в гг и во всех комнатах увеличивают fund и fund_acc одинаково
    """Покупка билета на разных уровнях"""

    @pytest.mark.parametrize("room_id", ["Air Test", "Pool", "Fork"])
    def test_funds_after_purchase_tickets(self, room_id):
        # получаем значения из статистики до покупки
        old_fund, old_fund_acc, royalty = self.refresh_statistic()

        self.buy_ticket(room_id=room_id)
        time.sleep(3)
        # проверка изменения дохода в fund и fund_acc после покупки билета
        self.assert_fund_income(old_fund, old_fund_acc, 1)

    """Покупка всех бустеров на разных уровнях"""

    @pytest.mark.parametrize("room_id, booster_id, booster_cost",
                             [("Air Test", 3, 5), ("Pool", 4, 10), ("Fork", 5, 25),
                              ("Air Test", 6, 100), ("Pool", 7, 50), ("Fork", 8, 10)])
    def test_funds_after_purchase_boosters(self, room_id, booster_id, booster_cost):

        # получаем значения из статистики до покупки
        old_fund, old_fund_acc, royalty = self.refresh_statistic()
        # покупка booster
        self.buy_booster(booster_id, room_id)
        time.sleep(3)
        # проверка изменения дохода в fund и fund_acc после покупки бустеров
        self.assert_fund_income(old_fund, old_fund_acc, booster_cost)

    # проверка кол-ва роялти для раздачи на данный момент
    def test_total_royalties(self):
        # получение статистики
        fund, fund_acc, royalty = self.refresh_statistic()

        # избежать кейса, когда нет ничего к начислению
        if fund_acc <= 0:
            Checking.assert_values(0, royalty)
            self.buy_booster(booster_id=6, room_id="Pool")
            # снова запрашиваю статистику, чтобы обновить fund_acc_value
            fund, fund_acc, royalty = self.refresh_statistic()
            if fund_acc <= 0:
                raise ValueError("После покупки статистика не поменялась. Кейс FAILED")

        # Проверка корректности значения в роялти = fund_acc * на долю для роялти
        expected_royalty = fund_acc * 0.15015
        Checking.assert_values(expected_royalty, royalty)
        print("Royalty рассчитано верно")

    # Проверка, что после раздачи, acc_fund обнуляется и последующее кол-во роялти считает от обновленного значения
    def test_royalty_calculate_from_new_fund_acc(self):
        # запуск выплаты royalty, чтобы обновить fund_acc
        self.give_royalties()
        time.sleep(5)

        # получение статистики
        fund, fund_acc, royalty = self.refresh_statistic()

        # исключить возможность, чт на момент теста равны, нам важно, чтобы они были разные
        if fund == fund_acc:
            # покупаю бустер
            self.buy_booster(booster_id=6, room_id="Pool")
            time.sleep(3)
            # запускаю снова раздачу роялти
            self.give_royalties()
            time.sleep(5)

        # получение статистики
        fund, fund_acc, royalty = self.refresh_statistic()

        # если после покупки бустера и раздачи они по-прежнему равны, то тест провален.
        if fund <= fund_acc:
            raise ValueError("Условия теста не выполняются, тест FAILED")
        # покупаю бустер
        self.buy_booster(booster_id=6, room_id="Pool")
        time.sleep(2)
        # получение статистики
        fund, fund_acc, royalty = self.refresh_statistic()
        # получаю значения из полей статистики
        # Проверка корректности значения в роялти = fund_acc * на долю для роялти
        expected_royalty = fund_acc * 0.15015
        Checking.assert_values(expected_royalty, royalty)
        print("Royalty рассчитано верно")
        # запускаю снова раздачу роялти
        self.give_royalties()
        time.sleep(5)
        # получение статистики
        fund, fund_acc, royalty = self.refresh_statistic()
        # получаю значения из полей статистики
        # проверка, что fund_acc_value и royalty_value обновились, fund осталось больше 0
        assert fund > 0, "Возможна ошибка"
        assert fund_acc == 0, "Возможна ошибка"
        assert royalty == 0, "Возможна ошибка"
        print("Значения в статистике обнулились")