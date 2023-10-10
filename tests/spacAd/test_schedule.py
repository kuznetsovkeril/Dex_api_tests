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
                # текущим расписанием я указываю в самом тесте в schedule. Теперь есть вариант подтягивать из апи

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
        return True

    def test_spacad_schedule(self):
        # получаем текущее расписание
        schedule = self.get_schedule()
        # что ожидаем получить. Если по расписанию сейчас закрыто, то вернет False, если открыто True
        expected_response = self.is_schedule_open(schedule)
        # что получим, если будем проситься в ивент заданной почтой
        email = "k.test@fexbox.org"  # всегда почта, которая есть в вайт листе
        result_response = self.is_eligible(email)  # фактический результат
        print(f'Actual: {result_response}')
        print(f'Expected: {expected_response}')
        # просто сравниваем два значения
        Checking.assert_values(expected_response, result_response)

        # проверка, что если расписание открыто, то open_hours не Null, если закрыто то Null (None)
        if result_response or expected_response is False:
            open_hours = False
            assert open_hours == self.if_open_hours(), "Ошибка в текущем расписании"
            print("Fasle. Расписания на сейчас нет, так как ивент недоступен")
        else:
            open_hours = True
            assert open_hours == self.if_open_hours(), "Ошибка в текущем расписании"
            print("True. Расписание не NULL, так как ивент доступен")



    """Тест юзера, который не входит в white list"""

    def test_non_white_list_user(self):
        pass


