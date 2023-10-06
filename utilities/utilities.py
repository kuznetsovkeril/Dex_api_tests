import uuid  # модуль для создания уникальной стройки
import random


class Instruments:

    """Метод генерации уникальных email"""

    @staticmethod
    def generate_unique_email():
        unique_str = str(uuid.uuid4())[:3]  # генерирует уникальную строку для мейла, чтобы почты всегда были уникальны
        email = f'test_mail_{unique_str}@fexbox.org'
        return email

    """Метод для сравнения значений с допустимым отклонением"""

    @staticmethod
    def approximately_equal(x, y, tolerance):
        return abs(x - y) <= tolerance

    # value1 = 200
    # value2 = 250
    #
    # # пример использования
    # if approximately_equal(value1, value2, tolerance=1000):
    #     print("Значения приблизительно равны.")
    # else:
    #     print("Значения не равны.")

    """Метод для округления суммы после запятой"""
    @staticmethod
    def round_num(value, index):
        # index = кол-во знаков до которого надо округлить
        # value = округляемое значение
        num = value
        round_num = round(num, index)  # Округляем до двух знаков после запятой
        print(round_num)

    """Метод генерации рандомного 4х-значного числа"""
    @staticmethod
    def random_num(self):
        random_number = random.randint(100, 999)
        print(random_number)

    @staticmethod
    def round_num(value, index):
        # index = кол-во знаков до которого надо округлить
        # value = округляемое значение
        num = value
        round_num = round(num, index)  # Округляем до двух знаков после запятой
        print(round_num)
