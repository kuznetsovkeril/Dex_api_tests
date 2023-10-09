import time

import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
import datetime
from src.auth_tokens import AUTH_BUY_GG_ITEMS
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

    @staticmethod
    def get_transaction(auth_token):


    """Проверка ответа статистики"""  # статус код, все поля присутствуют, дата = сегодня

    def test_royalties_statistics(self):
        a = 10


# Тест кейсы:
#  - расчет у юзера с 1 гравити нфт (и она куплена) - 	test_mail_57f@fexbox.org
#  - расчет у юзера с подарочными и купленными нфт (1 подарок + 1 куплена) - bonusnft2@fexbox.org
#  - расчет у юзера с несколькими гравити нфт (куплены пакетно и поштучно) + есть другие нфт (они не учет) - kirtest@fexbox.org
#  - расчет у юзера без гравити нф (но есть другие нфт) - vitabrevis@mailto.plus
#  - отсутствие транзакции при rouyalty = 0
# План: насобирать покупок, зафиксировать royalties. Посчитать у каждого пользователя и все это через параметризацию
#  - новые юзеры кто покупает, тоже получает нфт
