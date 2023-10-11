import json
from datetime import datetime

from utilities.api import Spacad_api
from utilities.checking import Checking
from utilities.getters import Getters


class TestSpacAdSchedule:
    """Проверка работы расписания"""  # скорее всего это будет актуально и для прода

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

    # получение текущего заданного расписания
    @staticmethod
    def get_schedule():
        result_schedule = Spacad_api.get_event_schedule()  # получаю ответ с расписанием
        Checking.check_status_code(result_schedule, 200)  # проверяю статус код ответа
        data = json.loads(result_schedule.text)  # преобразование json в текст
        schedule = []  # инициализация списка для расписания
        # выборка начала и конца ивента из каждого объекта
        for item in data["data"]:
            schedule.append((item["start"], item["end"]))
        print(f'Current schedule: {schedule}')
        return schedule

    # проверяю ответ для открытого и закрытого расписания
    @staticmethod
    def if_open_hours():
        result = Spacad_api.if_event_open_hours()
        Checking.check_status_code(result, 200)
        open_hours_response = Getters.get_json_field_value_0(result, "data")
        if open_hours_response is None:
            return False
        else:
            return True

    # метод проверки, что текущие часы расписания верные, если расписание открыто
    @staticmethod
    def check_current_hours():
        result = Spacad_api.if_event_open_hours()  # запрашиваю текущее время
        Checking.check_status_code(result, 200)
        current_time = datetime.utcnow().strftime("%H:%M:%S")  # получаю текущее время в UTC, тк с бэка данные в UTC
        print(f'UTC Time Now: {current_time}')
        print(f'Получения текущих часов открытия:')
        current_start_time = Getters.get_json_field_value_2(result, "data",
                                                            "start")  # получаю начало для текущего ивента
        current_end_time = Getters.get_json_field_value_2(result, "data", "end")  # получаю конец для текущего ивента
        # если настоящее время находится в рамках текущего расписания -> True, иначе False
        if current_start_time <= current_time <= current_end_time:
            return True
        else:
            return False

    def test_spacad_schedule(self):
        # получаем текущее расписание
        schedule = self.get_schedule()
        # Что ожидаем получить. Если по расписанию сейчас закрыто, то вернет False, если открыто True
        expected_response = self.is_schedule_open(schedule)
        # что получим, если будем проситься в ивент заданной почтой
        email = "k.test@fexbox.org"  # всегда почта, которая есть в вайт листе
        result_response = self.is_eligible(email)  # фактический результат
        print(f'Actual: {result_response}')
        print(f'Expected: {expected_response}')
        # просто сравниваем два значения
        Checking.assert_values(expected_response, result_response)

    # проверка, что если расписание открыто, то open_hours не Null, если закрыто то Null (None)
    def test_schedule_current_hours(self):
        # получаем текущее расписание
        schedule = self.get_schedule()
        # Что ожидаем получить. Если по расписанию сейчас закрыто, то вернет False, если открыто True
        expected_response = self.is_schedule_open(schedule)
        # что получим, если будем проситься в ивент заданной почтой
        email = "k.test@fexbox.org"  # всегда почта, которая есть в вайт листе
        result_response = self.is_eligible(email)  # фактический результат
        print(f'Actual: {result_response}')
        print(f'Expected: {expected_response}')
        if result_response is False and expected_response is False:
            open_hours = False
            print(f'Статус открытия текущего расписания: {self.if_open_hours()}')
            assert open_hours == self.if_open_hours(), "Ошибка в текущем расписании"
            print("False. Расписания на сейчас нет, так как ивент недоступен")
        elif result_response != expected_response:
            result = Spacad_api.if_event_open_hours()
            open_hours = Getters.get_json_field_value_0(result, "data")
            print(f'Текущее расписание: {open_hours}')
            raise ValueError("Ошибка в расписании! Кейс BROKEN")
        else:
            open_hours = True
            print(f"Статус открытия текущего расписания: {self.if_open_hours()}")
            assert open_hours == self.if_open_hours(), "Ошибка в текущем расписании"
            print("True. Расписание не NULL, так как ивент доступен")
            # проверить, что в случае открытия расписания текущее время находится в рамках этих часов
            current_hours = self.check_current_hours()  # заранее написанный метод проверки часов открытия, см выше
            print(f"Статус проверки текущих часов открытия: {current_hours}")
            assert current_hours is True, "Неверное время текущего расписания"
            print("Время текущего расписания верное.")

    """Тест юзера, который не входит в white list"""

    # def test_non_white_list_user(self):
    #     pass
