import time
from datetime import datetime, timedelta

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture(scope="module")
def email():
    return EMAIL_SPACAD_WHITELISTED


@pytest.fixture(scope="module")  #
def signature():
    return WATCH_SIGNATURE


@pytest.fixture(scope="module")
def first_watch(email, signature):
    # проверяю, что у юзера нет новой сессии, иначе будет дожидаться пока не закончится
    while True:
        result = Spacad_api.current_session(email)
        data = Getters.get_json_field_value_0(result, "data")
        if data is None:
            print("Session is finished.")
            break
        else:
            print("Session not finished yet.")
            time.sleep(20)

    result_watch = Spacad_api.watch(email, signature)  # собираю первую монетку
    Checking.check_status_code(result, 200)
    yield result_watch


class TestUserSession:

    # последующий сбор монетки
    @staticmethod
    def next_watch(email, signature):
        result = Spacad_api.watch(email, signature)  # собираю первую монетку
        Checking.check_status_code(result, 200)
        data = Getters.get_json_field_value_0(result, "data")
        print(f'WATCH data: {data}')
        return data

    # получение сессии пользователя
    @staticmethod
    def current_session(email):
        result = Spacad_api.current_session(email)
        Checking.check_status_code(result, 200)
        data = Getters.get_json_field_value_0(result, "data")
        print(f'SESSION data: {data}')
        return data

    """Проверка сессии пользователя"""

    # проверка времени начала сессии
    def test_session_create_time(self, set_spacad_ad, first_watch):
        result = first_watch

        # получаю текущий тайм - время отправки запроса
        watch_time_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        watch_time = datetime.strptime(watch_time_str, "%Y-%m-%d %H:%M:%S")

        # беру время начала квеста из пререквеста просмотра
        created_at_str = Getters.get_json_field_value_2(result, "data", "created_at")
        created_at = datetime.strptime(created_at_str.replace('T', ' ').replace(".000000Z", ''), "%Y-%m-%d %H:%M:%S")

        # высчитываю разницу между временем отправкой запроса и временем создания
        dif_start_time = watch_time - created_at
        assert timedelta(seconds=0) <= dif_start_time <= timedelta(seconds=2), "Временя не совпало"
        print("Время начала сессии корректное")

    def test_session_expire_time(self, set_spacad_ad, first_watch):
        result = first_watch

        created_at_str = Getters.get_json_field_value_2(result, "data", "created_at")
        created_at = datetime.strptime(created_at_str.replace('T', ' ').replace(".000000Z", ''), "%Y-%m-%d %H:%M:%S")

        expire_at_str = Getters.get_json_field_value_2(result, "data", "expire_at")
        expire_at = datetime.strptime(expire_at_str, "%Y-%m-%d %H:%M:%S")

        time_dif = expire_at - created_at

        # разница между началом сессии и ее концом должна быть равна 5 минутам (дев)
        expected_dif = timedelta(minutes=5)
        Checking.assert_values(expected_dif, time_dif)

    # проверяется данные в полях сессии и в полях ответа запроса сбора монет
    def test_session_data(self, first_watch, email, signature):
        result = first_watch  # это data первого сбора монеты
        first_watch_data = Getters.get_json_field_value_0(result, "data")

        # получаю id сессии первого запроса
        session_id = Getters.get_json_field_value_2(result, "data", "id")

        """STEP 1"""
        # проверяю, что кол-во монет = 1
        coins_first = Getters.get_json_field_value_2(result, "data", "coins")
        Checking.assert_values(1, coins_first)

        # проверяю, что данные в ответе первого запроса сбора монет = данным запроса сессии
        current_session = self.current_session(email)
        Checking.assert_values(current_session, first_watch_data)

        """STEP 2"""

        # проверка, что в сессии прибавилась еще одна монетка
        previous_coins = current_session["coins"]
        time.sleep(56)

        next_watch = self.next_watch(email, signature)  # собираю вторую монетку
        coins_new = next_watch["coins"]
        Checking.assert_values(previous_coins + 1, coins_new)

        # проверка, что после следующего сбора id не изменился

        # получаю id сессии следующего запроса
        session_id_watch = next_watch["id"]
        # сравниваю id сессии первого и второго сбора
        Checking.assert_values(session_id, session_id_watch)

        # проверяю, что данные в ответе второго запроса сбора монет = данным запроса сессии
        Checking.assert_values(next_watch, self.current_session(email))

        """STEP 3"""  # аналогичный шагу 2
        session_2 = self.current_session(email)
        previous_coins_2 = session_2["coins"]
        time.sleep(58)
        next_watch_3 = self.next_watch(email, signature)  # собираю вторую монетку
        coins_new_3 = next_watch_3["coins"]
        Checking.assert_values(previous_coins_2 + 1, coins_new_3)
        Checking.assert_values(next_watch_3, self.current_session(email))
        session_id_watch_3 = next_watch_3["id"]
        Checking.assert_values(session_id, session_id_watch_3)
        Checking.assert_values(next_watch_3, self.current_session(email))

        """STEP 4"""  # после неуспешного сбора данные сессии не изменятся
        session_3 = self.current_session(email)
        time.sleep(30)
        print("ОЖИДАНИЕ 30 СЕКНУДОВ")
        next_watch_4 = self.next_watch(email, signature)
        assert next_watch_4 is False
        Checking.assert_values(session_3, self.current_session(email))

    # def test_session_finish(self, first_watch, email, signature):
    #     # Дождаться окончания сессии, проверить, что следующая сессия не началась, пока не собрал некст монетку
