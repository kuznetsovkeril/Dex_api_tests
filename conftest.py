import time
from datetime import timedelta, datetime

import pytest
from playwright.sync_api import sync_playwright

from utilities.api import Spacad_api
from utilities.getters import Getters


@pytest.fixture(scope="function")
def wait_between_tests():
    delay = 20
    time.sleep(delay)


@pytest.fixture(scope="module")
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
                "args": "PlaySpacAD",
                "collect_coins": "1"
            }
        ]
    }
    Spacad_api.set_working_hours(start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"), settings)
    time.sleep(3)
    print("Расписание установлено")
    yield
    Spacad_api.refresh_working_hours("23:00:00", "23:59:59")
    # возвращение предыдущего расписания
    print("Вернул расписание обратно")


@pytest.fixture(scope="function")
def check_session(email):
    # проверяю текущую сессию пользователя
    while True:
        result = Spacad_api.current_session(email)
        data = Getters.get_json_field_value_0(result, "data")
        if data is None:
            print("Session is finished.")
            break
        else:
            print("Session not finished yet.")
            time.sleep(20)


# launch and close browser
@pytest.fixture()
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()
