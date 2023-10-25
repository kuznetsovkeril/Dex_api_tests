import time
from datetime import timedelta, datetime

import pytest

from utilities.api import Spacad_api


@pytest.fixture(scope="function")
def wait_between_tests():
    delay = 20
    time.sleep(delay)


@pytest.fixture()
def set_spacad_ad():
    # установка расписания
    start_time = datetime.utcnow()  # получаю текущее время utc
    end_time = start_time + timedelta(hours=1)  # прибавляю 1 час для окончания ивента
    # создаю слот расписания
    Spacad_api.set_working_hours(start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"), [])
    # задаю для этого слота settings
    settings = {
        "actions": [
            {
                "action": "invokeCustomEvent",
                "target": "",
                "args": "PlaySpacAD"
            }
        ]
    }
    Spacad_api.set_working_hours(start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"), settings)
    print("Расписание установлено")
    yield
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # возвращение предыдущего расписания
    print("Вернул расписание обратно")
