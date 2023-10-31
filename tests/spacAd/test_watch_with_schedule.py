import time
from datetime import datetime, timedelta

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture()
def set_schedule(request):
    settings, test_name, status_code_eligible, status_code_watch, eligible_field, email, signature = request.param
    # установка расписания
    start_time = datetime.utcnow().strftime("%H:%M:%S")
    end_time = (datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S")
    Spacad_api.set_working_hours(start_time, end_time, [])
    # задаю для этого слота settings
    Spacad_api.set_working_hours(start_time, end_time, settings)
    print(f"Расписание установлено для теста: {test_name}")
    yield status_code_eligible, status_code_watch, eligible_field, email, signature  # возвращаем эти значения для использования их в функции
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # откат расписания
    print(f"Откатил расписание после теста: {test_name}")


@pytest.fixture()
def set_schedule_closed(request):
    settings, status_code_eligible, status_code_watch, eligible_field, email, signature = request.param
    # установка расписания
    start_time = (datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S")
    end_time = (datetime.utcnow() + timedelta(hours=2)).strftime("%H:%M:%S")
    Spacad_api.set_working_hours(start_time, end_time, [])
    # задаю для этого слота settings
    Spacad_api.set_working_hours(start_time, end_time, settings)
    print(f"Расписание установлено для теста")
    yield status_code_eligible, status_code_watch, eligible_field, email, signature  # возвращаем эти значения для использования их в функции
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # откат расписания
    print(f"Откатил расписание после теста")


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

    @pytest.mark.parametrize("set_schedule",
                             [(settings_PlaySpacAD, "Test working hours for SpacAd ad", 200, 200, "data",
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE),
                              (settings_PlayGravity, "Test working hours for NONE-SpacAd ad", 200, 403, "data",
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE),
                              (settings_PlayNothing, "Test working hours without ad", 200, 403, "data",
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE),
                              (settings_PlayAdult, "Test watch adult ad with KYC", 200, 200, "data",
                               EMAIL_SPACAD_KYC, SPACAD_KYC_SIGNATURE),
                              (settings_PlayAdult, "Test watch adult without KYC", 200, 403, "data",
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)
                              ],
                             indirect=True)
    def test_watch_and_access_critical_path(self, set_schedule):
        status_code_eligible, status_code_watch, eligible_field, email, signature = set_schedule  # определяем значения переменных из фикстуры
        # вход в пространство
        result_eligible = Spacad_api.is_eligible(email=email)
        Checking.check_status_code(result_eligible, status_code_eligible)
        # проверяем тело ответа
        expected_result = True
        actual_result = Getters.get_json_field_value_0(result_eligible, eligible_field)
        Checking.assert_values(expected_result, actual_result)

        # сбор монеты
        result_watch = Spacad_api.watch(email=email, signature=signature)
        Checking.check_status_code(result_watch, status_code_watch)
        time.sleep(60)  # ожидание перед каждым сбором для 100% избежания конфликта сбора монет

    @pytest.mark.parametrize("set_schedule_closed",
                             [(settings_PlaySpacAD, 403, 403, "is_finished",
                               EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)], indirect=True)
    def test_access_schedule_closed(self, set_schedule_closed):
        status_code_eligible, status_code_watch, eligible_field, email, signature = set_schedule_closed  # определяем значения переменных из фикстуры
        # вход в пространство
        result_eligible = Spacad_api.is_eligible(email=email)
        Checking.check_status_code(result_eligible, status_code_eligible)
        # проверяем тело ответа
        expected_result = True
        actual_result = Getters.get_json_field_value_0(result_eligible, eligible_field)
        Checking.assert_values(expected_result, actual_result)

        # сбор монеты
        result_watch = Spacad_api.watch(email=email, signature=signature)
        Checking.check_status_code(result_watch, status_code_watch)
        # тут нужно проверить респонс что event Event doesn't start yet.!!!

    def test_collect_coins(self):
        pass

    def test_for_adults(self):
        pass
