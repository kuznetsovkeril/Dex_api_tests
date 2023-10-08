import time

import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
import datetime
from src.auth_tokens import AUTH_BUY_GG_ITEMS
from utilities.getters import Getters


class TestRoyalties:
    """Проверка фичи раздачи Royalties"""

    #  statistic_field_value = Getters.get_json_field_value_0(result, field_name)

    """Проверка ответа запроса статистики"""  # статус код, все поля присутствуют, дата = сегодня

    @pytest.mark.skip
    def test_royalties_statistics(self):
        # получение статистики
        result = Dexart_api.royalties_statistics()
        Checking.check_status_code(result, 200)
        # проверка что поле date = today date
        statistic_date = Getters.get_json_field_value_0(result, "date")
        today_date = datetime.date.today()
        print("Текущая дата:", today_date)
        Checking.assert_values(str(today_date), statistic_date)

    # проверка, что все виды покупок в гг и во всех комнатах увеличивают Fund

    @pytest.mark.parametrize("room_id, booster_id, booster_cost", [("Air Test", 3, 5), ("Pool", 6, 100)])
    def test_statistic_fund(self, room_id, booster_id, booster_cost):
        result = Dexart_api.royalties_statistics()
        # текущее значение в поле fund
        current_fund_value = Getters.get_json_field_value_0(result, "fund")

        """Покупка билета в Air Test и Pool"""

        result_buy_ticket = Dexart_api.ticket_buy(AUTH_BUY_GG_ITEMS, room_id=room_id)
        print(f'Room ID: {room_id}')
        Checking.check_status_code(result_buy_ticket, 200)
        # если у юзера уже куплен билет на этот день, этот шаг скипается и переходим к покупке билета в Pool
        try:
            check_message = Getters.get_json_field_value_2(result_buy_ticket, "data", "message")
            # проверка, что билет куплен, тогда в fund +0
            if check_message == "Already have a tiket":
                expected_fund_income = 0

                time.sleep(3)

                new_result = Dexart_api.royalties_statistics()
                new_fund_value = Getters.get_json_field_value_0(new_result, "fund")
                expected_fund_income = current_fund_value + expected_fund_income
                Checking.assert_values(expected_fund_income, new_fund_value)
        # если поле с сообщением не найдено, считаем, что билет куплен, и в fund + 1
        except KeyError:
            expected_fund_income = 1
            print("Билет успешно куплен")

            time.sleep(3)

            new_result = Dexart_api.royalties_statistics()
            new_fund_value = Getters.get_json_field_value_0(new_result, "fund")
            expected_fund_income = current_fund_value + expected_fund_income
            Checking.assert_values(expected_fund_income, new_fund_value)

        """Покупка бустеров в разных комнатах"""
        result = Dexart_api.royalties_statistics()
        # текущее значение в поле fund
        current_fund_value = Getters.get_json_field_value_0(result, "fund")

        result_buy_booster = Dexart_api.buy_booster(AUTH_BUY_GG_ITEMS, booster_id=booster_id, amount=1, room_id=room_id)
        print(f'Room ID: {room_id}')
        Checking.check_status_code(result_buy_booster, 200)
        print("Бустер успешно куплен")

        time.sleep(3)

        new_result = Dexart_api.royalties_statistics()
        new_fund_value = Getters.get_json_field_value_0(new_result, "fund")
        expected_fund_income = current_fund_value + booster_cost
        Checking.assert_values(expected_fund_income, new_fund_value)

    # проверка кол-ва всех роялти к разадче на данный момент
    def test_total_royalties(self):
        # получение статистики
        result_statistics = Dexart_api.royalties_statistics()
        Checking.check_status_code(result_statistics, 200)
        # fund_acc/кол-во нфт
        fund_acc_value = Getters.get_json_field_value_0(result_statistics, "fund_acc")
        if fund_acc_value == 0:
            # buy booster
            pass
        else:
            b = 1

    @staticmethod
    def give_royalties():
        result = Dexart_api.give_royalties()
        Checking.check_status_code(result, 200)

    @staticmethod
    def give_royalties1():
        result = Dexart_api.give_royalties()
        Checking.check_status_code(result, 200)

# понадобится 2 юзера с гравити нфт и без нфт гравити, но с другими нфт
# test

# 1) статистика
# -проверить, что fund = air test + Pool +
# -проверить, что дата = нау +
# -fund_acc = то что должно быть выдано без учета первого
# -посчитать, сколько всего должно royalty выдано? Это и проверит тотал
# 2) проверить что правильно считает роялти
#     - юзер с нфт
#     - юзер без нфт
#     - юзер с другими нфт
# План:
# написать метод для получения каждого поля из статистики
