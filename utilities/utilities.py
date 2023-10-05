import uuid  # модуль для создания уникальной стройки


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
