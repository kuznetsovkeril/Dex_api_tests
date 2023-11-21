import uuid  # модуль для создания уникальной стройки
import random
import pyotp


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
        return abs(x - y) <= tolerance  # abs возвращает абсолютное значение, т е модуль разницы

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
        print(f'Rounded num: {round_num}')
        return round_num

    """Метод генерации рандомного числа"""

    @staticmethod  # генерация рандомного чилса в интервале от a и b
    def random_num(a, b):
        random_num = random.randint(a, b)
        return random_num

    """Метод округления числа"""
    @staticmethod
    def round_numm(value, index):
        # index = кол-во знаков до которого надо округлить
        # value = округляемое значение
        num = value
        round_num = round(num, index)  # Округляем до двух знаков после запятой
        print(round_num)

    """Генерация 2FA"""
    @staticmethod
    def generate_2fa_code(secret):
        # секретный ключ гугл auth
        secret_key = secret
        # создание объекта TOTP с использованием секретного ключа
        totp = pyotp.TOTP(secret_key)
        # генерация кода
        otp_code = totp.now()
        # Используйте otp_code в вашем автотесте
        print("Сгенерированный OTP-код:", otp_code)
        return otp_code
