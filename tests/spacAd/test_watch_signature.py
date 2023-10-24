import json
from datetime import datetime

import pytest

from config_check import *
from utilities.api import Spacad_api, Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters


@pytest.fixture()
def set_working_hours(auth):
    #установка расписание
    yield
    #возвращение предыдущего расписания


class TestAntiBotSignature:
    """Проверка подписи при отправке события просмотра рекламы"""  # на проде не проверить

    @staticmethod  # проверка, что доступ к мероприятию по времени AND вайт листу есть
    def is_eligible(email):
        result = Spacad_api.is_eligible(email)
        status_code = result.status_code  # если нет в вайтлисте - 403, если расписание не началось - 403, поэтому
        # проверяю по статус коду
        print(f'Status code = {status_code}')
        print(f'Email: {email}')
        if status_code == 200:  # возвращает True только при таком статус коде, все остальное - False
            return True
        else:
            return False

    @staticmethod  # как я ожидаю будет работать расписание для юзеров из вайт листа
    def is_schedule_open(schedule):
        current_time = datetime.utcnow().strftime("%H:%M:%S")  # получаю текущее время в UTC, тк с бэка данные в UTC,
        # мы будем сравниваться ними
        print(f'UTC Time Now: {current_time}')
        for start_time, end_time in schedule:
            if start_time <= current_time <= end_time:  # из расписания берет время начала и конца и сравнивает с
                # текущим расписанием, которое берем с бэка - это реальное действующее расписание
                return True
        # если совпадения нет, то вернуть false вне цикла
        return False
