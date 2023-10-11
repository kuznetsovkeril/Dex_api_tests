import time

import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
import datetime
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
        print("Статистика получена и обновлена")
        return result

    @staticmethod
    def assert_fund_income(old_fund_value, old_fund_acc_value, expected_income):

        result = Dexart_api.royalties_statistics()
        new_fund_value = Getters.get_json_field_value_0(result, "fund")
        new_fund_acc_value = Getters.get_json_field_value_0(result, "fund_acc")
        expected_fund_income = old_fund_value + expected_income
        print(f'Ожидаемое новое fund_income = {expected_fund_income}')
        Checking.assert_values(expected_fund_income, new_fund_value)
        expected_fund_acc_income = old_fund_acc_value + expected_income
        print(f'Ожидаемое новое fund_acc_income = {expected_fund_acc_income}')
        Checking.assert_values(expected_fund_acc_income, new_fund_acc_value)

    """Проверка ответа статистики"""  # статус код, все поля присутствуют, дата = сегодня

    def test_royalties_statistics(self):
        # получение статистики
        result = self.refresh_statistic()
        # проверка что поле date = today date
        statistic_date = Getters.get_json_field_value_0(result, "date")
        today_date = datetime.date.today()
        print("Текущая дата:", today_date)
        Checking.assert_values(str(today_date), statistic_date)
        # проверить, что все поля присутствуют
        result_fields = Checking.show_json_fields(result)
        expected_fields = ['date', 'fund', 'fund_acc', 'royalty', 'total_nfts']
        Checking.assert_values(expected_fields, result_fields)
        print("Необходимые поля присутствуют в ответе")

    # проверка, что кол-во нфт отдает примерно верное число (точно не получится сосчитать)
    def test_total_nfts(self):
        # получение статистики
        result = self.refresh_statistic()
        # получение total_nfts
        total_nfts = Getters.get_json_field_value_0(result, "total_nfts")
        assert total_nfts > 20000, "Неверное total_nft. Нужно проверить!"

    # проверка, что все виды покупок в гг и во всех комнатах увеличивают Fund и fund_acc одинаково
    @pytest.mark.parametrize("room_id, booster_id, booster_cost", [("Air Test", 3, 5), ("Pool", 6, 100)])
    def test_statistic_fund(self, room_id, booster_id, booster_cost):
        result = Dexart_api.royalties_statistics()
        # текущее значение в поле fund
        old_fund_value = Getters.get_json_field_value_0(result, "fund")
        old_fund_acc_value = Getters.get_json_field_value_0(result, "fund_acc")

        """Покупка билета в Air Test и Pool"""

        result_buy_ticket = Dexart_api.ticket_buy(AUTH_BUY_GG_ITEMS, room_id=room_id)
        print(f'Room ID: {room_id}')
        Checking.check_status_code(result_buy_ticket, 200)
        # если у юзера уже куплен билет на этот день, проверяем, что статистика не изменилась
        try:
            check_message = Getters.get_json_field_value_2(result_buy_ticket, "data", "message")
            # проверка, что билет куплен, тогда в fund +0
            if check_message == "Already have a tiket":

                time.sleep(3)
                # проверка изменения дохода в fund и fund_acc после покупки билетов
                self.assert_fund_income(old_fund_value, old_fund_acc_value, 0)
        # если поле с сообщением не найдено, считаем, что билет куплен, и в fund + 1
        except KeyError:
            # цена одного билета 1 DXA
            print("Билет успешно куплен")

            time.sleep(3)
            # проверка изменения дохода в fund и fund_acc после покупки билетов
            self.assert_fund_income(old_fund_value, old_fund_acc_value, 1)

        """Покупка бустеров в разных комнатах"""

        # запрос статистики
        result = Dexart_api.royalties_statistics()
        # текущее значение в поле fund
        old_fund_value = Getters.get_json_field_value_0(result, "fund")
        old_fund_acc_value = Getters.get_json_field_value_0(result, "fund_acc")
        # покупка booster
        self.buy_booster(booster_id, room_id)

        time.sleep(3)
        # проверка изменения дохода в fund и fund_acc после покупки бустеров
        self.assert_fund_income(old_fund_value, old_fund_acc_value, booster_cost)

    # проверка кол-ва роялти для раздачи на данный момент
    def test_total_royalties(self):
        # получение статистики
        result_statistics = self.refresh_statistic()

        # получаю значения из полей статистики
        fund_acc_value = Getters.get_json_field_value_0(result_statistics, "fund_acc")
        royalty_value = Getters.get_json_field_value_0(result_statistics, "royalty")
        # избежать кейса, когда нет ничего к начислению
        if fund_acc_value <= 0:
            self.buy_booster(booster_id=6, room_id="Pool")
            # снова запрашиваю статистику, чтобы обновить fund_acc_value
            result_statistics = Dexart_api.royalties_statistics()
            fund_acc_value = Getters.get_json_field_value_0(result_statistics, "fund_acc")
            royalty_value = Getters.get_json_field_value_0(result_statistics, "royalty")
            if fund_acc_value <= 0:
                raise ValueError("После покупки статистика не поменялась. Кейс FAILED")

        # Проверка корректности значения в роялти = fund_acc * на долю для роялти
        expected_total_royalty = fund_acc_value * 15.015 / 100
        Checking.assert_values(expected_total_royalty, royalty_value)
        print("Royalty рассчитано верно")

    # Проверка, что после раздачи, acc_fund обнуляется и последующее кол-во роялти считает от обновленного значения
    def test_royalty_calculate_from_new_fund_acc(self):
        # запуск выплаты royalty, чтобы обновить fund_acc
        self.give_royalties()
        time.sleep(5)

        # получение статистики
        result_statistics = self.refresh_statistic()

        # получаю значения из полей статистики
        fund_value = Getters.get_json_field_value_0(result_statistics, "fund")
        fund_acc_value = Getters.get_json_field_value_0(result_statistics, "fund_acc")
        # исключить возможность, чт на момент теста равны, нам важно, чтобы они были разные
        if fund_value == fund_acc_value:
            # покупаю бустер
            self.buy_booster(booster_id=6, room_id="Pool")
            time.sleep(3)
            # запускаю снова раздачу роялти
            self.give_royalties()
            time.sleep(5)

        # получение статистики
        result_statistics = self.refresh_statistic()

        # получаю значения из полей статистики
        fund_value = Getters.get_json_field_value_0(result_statistics, "fund")
        fund_acc_value = Getters.get_json_field_value_0(result_statistics, "fund_acc")

        # если после покупки бустера и раздачи они по-прежнему равны, то тест провален.
        if fund_value <= fund_acc_value:
            raise ValueError("Условия теста не выполняются, тест FAILED")
        # покупаю бустер
        self.buy_booster(booster_id=6, room_id="Pool")
        time.sleep(2)
        # получение статистики
        result_statistics = self.refresh_statistic()
        # получаю значения из полей статистики
        fund_acc_value = Getters.get_json_field_value_0(result_statistics, "fund_acc")
        royalty_value = Getters.get_json_field_value_0(result_statistics, "royalty")
        # Проверка корректности значения в роялти = fund_acc * на долю для роялти
        expected_total_royalty = fund_acc_value * 15.015 / 100
        Checking.assert_values(expected_total_royalty, royalty_value)
        print("Royalty рассчитано верно")
        # запускаю снова раздачу роялти
        self.give_royalties()
        time.sleep(5)
        # получение статистики
        result_statistics = self.refresh_statistic()
        # получаю значения из полей статистики
        fund_value = Getters.get_json_field_value_0(result_statistics, "fund")
        fund_acc_value = Getters.get_json_field_value_0(result_statistics, "fund_acc")
        royalty_value = Getters.get_json_field_value_0(result_statistics, "royalty")
        # проверка, что fund_acc_value и royalty_value обновились, fund осталось больше 0
        assert fund_value > 0, "Возможна ошибка"
        assert fund_acc_value == 0, "Возможна ошибка"
        assert royalty_value == 0, "Возможна ошибка"
        print("Значения в статистике обнулились")

    # проверка, что royalty = 0, если fund_acc_value = 0
    def test_zero_total_royalties(self):
        # запуск выплаты royalty, чтобы обновить fund_acc
        self.give_royalties()
        time.sleep(5)
        # получение статистики
        result_statistics = self.refresh_statistic()
        # проверка, что fund_acc = 0
        fund_acc_value = Getters.get_json_field_value_0(result_statistics, "fund_acc")
        assert fund_acc_value == 0, "Ошибка. Fund_acc > 0"
        print("fund_acc_value = 0")
        royalty_value = Getters.get_json_field_value_0(result_statistics, "royalty")
        # Проверка корректности значения в роялти роялти = fund_acc * на долю для роялти
        expected_total_royalty = 0
        Checking.assert_values(expected_total_royalty, royalty_value)
