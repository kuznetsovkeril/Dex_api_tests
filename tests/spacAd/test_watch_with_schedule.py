import time
from datetime import datetime, timedelta

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture()
def set_schedule(request):
    settings, test_name, status_code_eligible, status_code_watch, email, signature = request.param
    # установка расписания
    start_time = datetime.utcnow().strftime("%H:%M:%S")
    end_time = (datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S")
    Spacad_api.set_working_hours(start_time, end_time, [])
    # задаю для этого слота settings
    Spacad_api.set_working_hours(start_time, end_time, settings)
    time.sleep(3)
    print(f"Расписание установлено для теста: {test_name}")
    yield status_code_eligible, status_code_watch, email, signature  # возвращаем эти значения для использования их в функции
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # откат расписания
    print(f"Откатил расписание после теста: {test_name}")


@pytest.fixture()
def set_schedule_closed(request):
    settings, status_code_eligible, status_code_watch, email, signature = request.param
    # установка расписания
    start_time = (datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S")
    end_time = (datetime.utcnow() + timedelta(hours=2)).strftime("%H:%M:%S")
    Spacad_api.set_working_hours(start_time, end_time, [])
    # задаю для этого слота settings
    Spacad_api.set_working_hours(start_time, end_time, settings)
    print(f"Расписание установлено для теста")
    time.sleep(3)
    yield status_code_eligible, status_code_watch, email, signature  # возвращаем эти значения для использования их в функции
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # откат расписания
    print(f"Откатил расписание после теста")


@pytest.fixture()
def set_schedule_params(request):
    for_adults, collect_coins, test_name, status_code_eligible, \
        status_code_watch, email, signature, wait_time = request.param
    # настройки для слота расписания
    settings = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlaySome",
                "for_adults": for_adults,
                "collect_coins": collect_coins

            }
        ]
    }
    # установка расписания
    start_time = datetime.utcnow().strftime("%H:%M:%S")
    end_time = (datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S")
    Spacad_api.set_working_hours(start_time, end_time, [])
    # задаю для этого слота settings
    Spacad_api.set_working_hours(start_time, end_time, settings)
    print(f"Расписание установлено для теста: {test_name}")
    time.sleep(3)
    yield status_code_eligible, status_code_watch, email, signature, wait_time  # возвращаем эти значения для использования их в функции
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # откат расписания
    print(f"Откатил расписание после теста: {test_name}")


@pytest.mark.skip(reason="The Project has been stopped")
class TestWatchWithSchedule:
    """Проверка отправки события и доступа к мероприятию при различном расписании"""  # на проде не проверить

    # реклама спакада
    settings_PlaySpacAD = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlaySpacAD",
                "collect_coins": "1"
            }
        ]
    }

    # расписание просто открыто
    settings_PlayNothing = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": []
            }
        ]
    }

    # реклама без сбора монет
    settings_PlayGravity = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlayGravity"
            }
        ]
    }

    # реклама для юзеров с KYC
    settings_PlayAdult = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlayAdult",
                "for_adults": "1",
                "collect_coins": "1"
            }
        ]
    }

    settings_for_collect_coins = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlaySpacAD",
                "collect_coins": "1"
            }
        ]
    }

    @staticmethod
    def check_is_eligible(email, status_code, result_field_value):
        # вход в пространство
        result_eligible = Spacad_api.is_eligible(email=email)
        Checking.check_status_code(result_eligible, status_code)
        # проверяем тело ответа
        expected_result = True
        actual_result = Getters.get_json_field_value_0(result_eligible, result_field_value)
        Checking.assert_values(expected_result, actual_result)

    @staticmethod
    def check_watch(email, signature, status_code):
        result_watch = Spacad_api.watch(email=email, signature=signature)
        Checking.check_status_code(result_watch, status_code)
        if status_code == 200:
            expected_fields = ['id', 'coins', 'max_limit', 'min_limit', 'coins_left', 'progress', 'expire_at',
                               'created_at']
            Checking.check_json_fields_in_v2(result_watch, "data", expected_fields)
        elif status_code == 403:
            watch_data = Getters.get_json_field_value_0(result_watch, "message")
            assert watch_data == "Event doesn't start yet"
        else:
            print("Something went wrong!")

    @pytest.mark.parametrize("set_schedule",
                             [(settings_PlaySpacAD, "Test working hours for SpacAd ad", 200, 200,
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE),
                              (settings_PlayGravity, "Test working hours for NONE-SpacAd ad", 200, 403,
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE),
                              (settings_PlayNothing, "Test working hours without ad", 200, 403,
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE),
                              (settings_PlayAdult, "Test watch adult ad with KYC", 200, 200,
                               EMAIL_SPACAD_KYC, SPACAD_KYC_SIGNATURE),
                              (settings_PlayAdult, "Test watch adult without KYC", 200, 403,
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)
                              ],
                             indirect=True)
    def test_watch_and_access_critical_path(self, set_schedule):
        status_code_eligible, status_code_watch, email, signature = set_schedule  # определяем значения переменных из фикстуры
        # вход в пространство
        self.check_is_eligible(email, status_code_eligible, "data")

        # сбор монеты
        self.check_watch(email, signature, status_code_watch)
        time.sleep(60)  # ожидание перед каждым сбором для 100% избежания конфликта сбора монет

    @pytest.mark.parametrize("set_schedule_closed",
                             [(settings_PlaySpacAD, 403, 403,
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)], indirect=True)
    def test_access_schedule_closed(self, set_schedule_closed):
        status_code_eligible, status_code_watch, email, signature = set_schedule_closed  # определяем значения переменных из фикстуры
        # вход в пространство
        self.check_is_eligible(email, status_code_eligible, "is_finished")

        # сбор монеты
        result_watch = Spacad_api.watch(email=email, signature=signature)
        Checking.check_status_code(result_watch, status_code_watch)
        watch_data = Getters.get_json_field_value_0(result_watch, "message")
        assert "Event doesn't start yet. Come after 59 minutes" in watch_data

    @pytest.mark.parametrize("set_schedule_params",
                             [("1", "1", "Test adults=1 collect=1 for user with KYC", 200, 200, EMAIL_SPACAD_KYC,
                               SPACAD_KYC_SIGNATURE, 1),
                              ("1", "1", "Test adults=1 collect=1 for user without KYC", 200, 403, EMAIL_SPACAD_WHITELISTED,
                               WATCH_SIGNATURE, 59),
                              ("1", "0", "Test adults=1 collect=0 for user with KYC", 200, 403, EMAIL_SPACAD_KYC,
                               SPACAD_KYC_SIGNATURE, 1),
                              ("1", "0", "Test adults=1 collect=0 for user without KYC", 200, 403, EMAIL_SPACAD_WHITELISTED,
                               WATCH_SIGNATURE, 59),
                              ("0", "1", "Test adults=0 collect=1 for user with KYC", 200, 200, EMAIL_SPACAD_KYC,
                               SPACAD_KYC_SIGNATURE, 1),
                              ("0", "1", "Test adults=0 collect=1 for user without KYC", 200, 200, EMAIL_SPACAD_WHITELISTED,
                               WATCH_SIGNATURE, 59),
                              (None, "0", "Test adults=Null collect=0 for user with KYC", 200, 403, EMAIL_SPACAD_KYC,
                               SPACAD_KYC_SIGNATURE, 1),
                              ("0", None, "Test adults=0 collect=Null for user without KYC", 200, 403, EMAIL_SPACAD_WHITELISTED,
                               WATCH_SIGNATURE, 59),
                              ],
                             indirect=True)
    def test_settings_args(self, set_schedule_params):
        status_code_eligible, status_code_watch, email, signature, wait_time = set_schedule_params  # определяем значения переменных из фикстуры
        # вход в пространство
        self.check_is_eligible(email, status_code_eligible, "data")

        # сбор монеты
        self.check_watch(email, signature, status_code_watch)

        time.sleep(wait_time)  # ожидание перед каждым сбором для 100% избежания конфликта сбора монет
