import time
from datetime import datetime

from utilities.api import Spacad_api
from utilities.checking import Checking


class TestSpacAdSchedule:

    """Проверка работы расписания"""  # скорее всего это будет актуально и для прода

    #     На текущий момент расписание такое:
    #     С 2 до 3 ночи по мск
    #     С 9 до 10 утра
    #     С 15-16 дня и
    #     С 22 до 23 часов.
    @staticmethod  # проверка, что доступ к мероприятию по времени AND вайт листу есть
    def is_eligible(email):
        result = Spacad_api.is_eligible(email)
        status_code = result.status_code  # если нет в вайтлисте - 403, если расписание не началось - 403, поэтому проверяю по статус коду
        print(f'Status code = {status_code}')
        print(f'Email: {email}')
        if status_code == 200:  # возвращает True только при таком статус коде, все остальное - False
            return True
        else:
            return False

    @staticmethod  # как я ожидаю будет работать расписание для юзеров из вайт листа
    def is_schedule_open(schedule):
        current_time = datetime.now().strftime("%H:%M:%S") # получаю текущее время в заданном формате
        print(f'Time Now: {current_time}')
        for start_time, end_time in schedule:
            print(f'Start: {start_time}')
            print(f'End: {end_time}')
            if start_time <= current_time <= end_time:  # из расписания берет время начала и конца и сравнивает с
                # текущим, расписание я указываю в самом тесте в schedule. Теперь есть вариант подтягивать из апи
                return True
        # если совпадения нет, то вернуть false вне цикла
        return False

    def test_spacad_schedule(self):
        # задаем текущее расписание
        schedule = [("13:36:00",  "13:37:00"), ("13:38:00",  "13:39:00"), ("13:41:00",  "13:42:00"), ("13:42:00",  "13:43:00")]
        # что ожидаем получить
        expected_response = self.is_schedule_open(schedule)
        # что получим, если будем проситься в ивент заданной почтой
        email = "k.test@fexbox.org"  # всегда почта, которая есть в вайт листе
        result_response = self.is_eligible(email)  # фактический результат
        print(f'Actual: {result_response}')
        print(f'Expected: {expected_response}')
        # просто сравниваем два значения
        Checking.assert_values(expected_response, result_response)

    """Написать тест для юзера, который не входит в вайт лист"""
    def test_non_white_list_user(self):
        # начало теста
        pass  # это удалить


