import time
from datetime import timedelta, datetime

import pytest
from playwright.sync_api import sync_playwright

from utilities.api import Spacad_api, Dexart_api
from utilities.checking import Checking
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


# buy and return parcel
@pytest.fixture()
def buy_parcel(auth_token, price_zone):
    result_parcel_list = Dexart_api.get_region_parcels("REGION-15")  # парсинг списка парселей из 15 района
    Checking.check_status_code(result_parcel_list, 200)
    parcel_id = Getters.get_parcel_by_status(result_parcel_list, status_id=1,
                                             price_zone=price_zone)  # выбирается свободный парсель со статусом 1
    result_add_parcel = Dexart_api.add_parcel_to_cart(auth_token, parcel_id=parcel_id)
    Checking.check_status_code(result_add_parcel, 200)
    print(f"Parcels {parcel_id} added to cart")
    # покупаю этот парсель с баланса для ускорения процесса тестирования
    result_buy_parcel = Dexart_api.buy_parcel(auth_token, driver="balance", email="some_user_email@fexbox.org")
    Checking.check_status_code(result_buy_parcel, 201)
    order_id = Getters.get_json_field_value_2(result_buy_parcel, "data", "id")
    yield str(order_id), parcel_id
    parcel_return = Dexart_api.return_parcel(parcel_ids=[parcel_id])
    Checking.check_status_code(parcel_return, 200)
    print("Parcel returned in stock")
