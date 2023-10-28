import json
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
        data = json.loads(result.text)["data"]
        if data is None:
            print("Session is finished.")
            break
        else:
            print("Session not finished yet.")
            time.sleep(20)

    result_watch = Spacad_api.watch(email, signature)  # собираю первую монетку
    Checking.check_status_code(result_watch, 200)
    result_watch_data = json.loads(result_watch.text)["data"]
    yield result_watch_data


class TestUserSession:

    #
    @staticmethod
    def get_current_time():
        current_time_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")
        return current_time

    @staticmethod
    def get_created_at(first_watch_result):
        created_at_str = first_watch_result["created_at"]
        print(first_watch_result)
        created_at = datetime.strptime(created_at_str.replace('T', ' ').replace(".000000Z", ''), "%Y-%m-%d %H:%M:%S")
        return created_at

    @staticmethod
    def get_expire_at(first_watch_result):
        expire_at_str = first_watch_result["expire_at"]
        expire_at = datetime.strptime(expire_at_str, "%Y-%m-%d %H:%M:%S")
        return expire_at

    # последующий сбор монетки
    @staticmethod
    def next_watch(email, signature):
        result = Spacad_api.watch(email, signature)  # собираю первую монетку
        Checking.check_status_code(result, 200)
        watch_data = json.loads(result.text)["data"]
        print(f'WATCH data: {watch_data}')
        return watch_data

    # получение сессии пользователя
    @staticmethod
    def current_session(email):
        result = Spacad_api.current_session(email)
        Checking.check_status_code(result, 200)
        session_data = json.loads(result.text)["data"]
        print(f'SESSION data: {session_data}')
        return session_data

    """Проверка сессии пользователя"""

    # проверка времени начала сессии
    def test_session_create_time(self, set_spacad_ad, first_watch):
        first_watch_result = first_watch
        # получаю текущий тайм - время отправки запроса
        watch_time = self.get_current_time()

        # беру время начала квеста из пререквеста первого просмотра
        created_at = self.get_created_at(first_watch_result)

        # высчитываю разницу между временем отправкой запроса и временем создания
        dif_start_time = watch_time - created_at
        assert timedelta(seconds=0) <= dif_start_time <= timedelta(seconds=2), "Временя начала сессии неверное!"
        print("Время начала сессии корректное")

    def test_session_expire_time(self, set_spacad_ad, first_watch):
        first_watch_result = first_watch

        created_at = self.get_created_at(first_watch_result)
        expire_at = self.get_expire_at(first_watch_result)

        # получаю разницу между окончанием и началом сессии
        time_dif = expire_at - created_at

        # проверяю, что разница между началом сессии и ее концом равна 5 минутам (дев)
        expected_dif = timedelta(minutes=5)
        Checking.assert_values(expected_dif, time_dif)

    # проверяются данные в полях сессии и в полях ответа запроса сбора монет
    def test_session_data(self, set_spacad_ad, first_watch, email, signature):
        result_first_watch = first_watch  # это data первого сбора монеты

        # получаю id сессии первого запроса
        session_id = result_first_watch["id"]

        """STEP 1"""
        # проверяю, что кол-во монет = 1
        coins_first = result_first_watch["coins"]
        Checking.assert_values(1, coins_first)

        # проверяю, что данные в ответе первого запроса сбора монет = данным запроса сессии
        current_session = self.current_session(email)
        Checking.assert_values(current_session, result_first_watch)

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

    def test_session_finish(self, set_spacad_ad, first_watch, email, signature):
        # дожидаемся окончания сессии и проверяем, что data = null и после можно начать новую сессию
        first_watch_result = first_watch  # это data первого сбора монеты
        current_time = self.get_current_time()
        expire_at = self.get_expire_at(first_watch_result)
        time_wait = (expire_at - current_time).total_seconds()
        print(f'Wait for {time_wait} seconds')
        time.sleep(time_wait + 2)

        # проверяю, что data текущей сессии = null
        check_session = self.current_session(email)
        assert check_session is None
        print("Сессия завершена")

        # начинаю новую сессию
        previous_session_id = first_watch_result # получаю id предыдущей сессии
        print(previous_session_id)
        new_session = self.next_watch(email, signature)
        new_session_id = new_session["id"]
        print(new_session_id)
        assert new_session_id > previous_session_id




