import time
from datetime import datetime, timedelta

import pytest

from config_check import *
from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture()
def set_schedule(request):
    start_time, end_time, settings, test_name, status_code_eligible, status_code_watch, eligible_field = request.param
    # установка расписания
    Spacad_api.set_working_hours(start_time, end_time, [])
    # задаю для этого слота settings
    Spacad_api.set_working_hours(start_time, end_time, settings)
    print(f"Расписание установлено для теста: {test_name}")
    yield status_code_eligible, status_code_watch, eligible_field  # возвращаем эти значения для использования их в функции
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # откат расписания
    print(f"Откатил расписание после теста: {test_name}")


class TestWatchWithSchedule:
    """Проверка отправки события и доступа к мероприятию при различном расписании"""  # на проде не проверить
    settings_1 = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlaySpacAD"
            }
        ]
    }
    settings_2 = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlayGravity"
            }
        ]
    }
    settings_3 = None

    @pytest.mark.parametrize("set_schedule", [
        (datetime.utcnow().strftime("%H:%M:%S"), (datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S"),
         settings_1, "Test working hours for SpacAd ad", 200, 200, "data"),
        (datetime.utcnow().strftime("%H:%M:%S"), (datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S"),
         settings_2, "Test working hours for NOT SpacAd ad", 200, 403, "data"),
        (datetime.utcnow().strftime("%H:%M:%S"), (datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S"),
         settings_3, "Test working hours without ad", 200, 403),
        ((datetime.utcnow() + timedelta(hours=1)).strftime("%H:%M:%S"),
         (datetime.utcnow() + timedelta(hours=2)).strftime("%H:%M:%S"),
         settings_3, "The event is closed", 403, 403, "is_finished")
    ], indirect=True)
    def test_watch_and_access(self, set_schedule):
        time.sleep(3)  # ожидание перед каждым сбором для 100% избежания конфликта сбора монет
        status_code_eligible, status_code_watch, eligible_field = set_schedule  # определяем значения переменных из фикстуры
        # вход в пространство
        result_eligible = Spacad_api.is_eligible(EMAIL_SPACAD_WHITELISTED)
        Checking.check_status_code(result_eligible, status_code_eligible)
        # проверяем тело ответа
        expected_result = True
        actual_result = Getters.get_json_field_value_0(result_eligible, eligible_field)
        Checking.assert_values(expected_result, actual_result)

        # сбор монеты
        result_watch = Spacad_api.watch(EMAIL_SPACAD_WHITELISTED, WATCH_SIGNATURE)
        Checking.check_status_code(result_watch, status_code_watch)

