import json
from pydantic import BaseModel

"""Проверка получаемых в ответе данных"""


class Checking():
    """Проверка статус кода"""

    @staticmethod
    def check_status_code(result, status_code):
        assert status_code == result.status_code, f'Статус код не прошел проверку. Получен код: {result.status_code}'
        print(f'Статус код прошел проверку. Код: {result.status_code}')

    """Метод проверки наличия обязательных полей в ответе"""

    @staticmethod # простая проверка на наличие полей
    def show_all_fields(result, field_1, field_2, index=None,):
        if index is not None:
            json_response = json.loads(result.text)  # возвращает json ответ
            data_items = json_response[field_1][field_2][index]
            print(list(data_items))
            return list(data_items)
        else:
            json_response = json.loads(result.text)  # возвращает json ответ
            data_items = json_response[field_1][field_2]
            print(list(data_items))
            return list(data_items)
    """Метод проверки наличия обязательных полей в ответе"""

    # парсинг имеющихся полей в ответе для конкретного объекта
    @staticmethod
    def show_json_fields(result, field_name_1=None):
        json_response = result.json()
        if field_name_1 is not None:
            for data_item in json_response[field_name_1]:  # Пробегаемся по каждому полю ответа во вложенном объекте
                fields_names = list(data_item)
                print(f'Поля в JSON ответе для массива {field_name_1}: {fields_names}')
                return fields_names
        else:
            data_item = json_response
            fields_names = list(data_item.keys())  # Получаем названия полей этого объекта
            print(f'Поля в JSON ответе: {fields_names}')
            return fields_names

    @staticmethod  # выводит названия всех полей для конкртеного объекта в ответе
    def show_json_fields_for_item(result, field_name_1, index):
        json_response = json.loads(result.text)
        data_item = json_response[field_name_1][index]  # Получаем объект с заданным индексом
        fields_names = list(data_item.keys())  # Получаем названия полей этого объекта
        print(f'Поля в JSON ответ для объекта #{index + 1} в массиве {field_name_1}: {fields_names}')
        return fields_names

    @staticmethod  # выводит названия всех полей для конкретного вложенного объекта в ответе
    def show_json_fields_for_in_item(result, field_name_1, index, field_name_2):
        json_response = json.loads(result.text)
        data_item = json_response[field_name_1][index][field_name_2]  # Получаем объект с заданным индексом
        fields_names = list(data_item)  # Получаем названия полей этого объекта
        print(f'Поля в JSON ответ для объекта #{index + 1} в массиве {field_name_1}, {field_name_2}: {fields_names}')
        return fields_names

    @staticmethod
    def check_json_fields_in(result, field_name_1, expected_value):
        json_response = json.loads(result.text)  # Преобразует JSON-ответ в объект Python
        for data_item in json_response[field_name_1]:  # Пробегаемся по каждому полю ответа
            print(list(data_item))  # Выводит на печать только поля json ответа в объекте data
            assert list(data_item) == expected_value, "Не все необходимые поля присутсвтуют в ответе"
        print("Все необходимы поля присутствуют в json ответе")

    # полностью аналогичен способу выше
    @staticmethod
    def check_json_fields_in_v2(result, field_name_1, expected_value):
        json_response = result.json()
        data_items = json_response[field_name_1]
        print(list(data_items))  # выводит названия всех полей в ответе
        assert (list(data_items)) == expected_value, "Не все необходимые поля присутсвтуют в ответе"
        print("Все необходимы поля присутствуют в json ответе")

    # проверяет наличие конкретного поля в ответе
    @staticmethod
    def check_one_field_in_json(result, field_name_1, field_name_2):
        json_response = json.loads(result.text)
        data = json_response.get(field_name_1, {})  # проваливаюсь в поле data в ответе
        if field_name_2 in data:  # ищу нужное вложенное поле
            print("Искомое вложенное поле присутствует в ответе")
        else:
            print(f'Искомое поле "{field_name_2}" в ответе не найдено')

    """Методы проверки значения поля в ответе"""

    @staticmethod
    def check_json_value(result, field_name_1, expected_value):
        check = result.json()  # выводим ответ в виде json
        check_value = check.get(field_name_1)  # получаем значение определенного поля из ответа
        print(f'Значение проверяемого поля "{field_name_1}": {check_value}')
        assert check_value == expected_value, "Полученное значение не совпадает с ожидаемым результатом."
        print(f'Проверка значения в поле пройдена.')

    # уровень вложенности 2
    @staticmethod
    def check_json_value_2(result, field_name_1, field_name_2, expected_value):
        check = result.json()  # выводим ответ в виде json
        check_value = check.get(field_name_1, {}).get(field_name_2)  # получаем значение определенного поля из ответа
        print(f'Значение проверяемого поля "{field_name_2}": {check_value}')
        assert check_value == expected_value, f'Ожидаемый результат не получен. Фактический результат: {check_value}'
        print(f'Проверка пройдена.')

    # Еще один метод для проверки наличия полей, но с другим типом данных - массив
    # нужно разобраться, скорее всего можно как то упростить
    @staticmethod
    def check_json_value_v2(result, field_name_1, field_name_2, expected_value):
        data = result.json().get(field_name_1)
        for item in data:
            check_value = item.get(field_name_2)
            print(f'Значение проверяемого поля "{field_name_2}": {check_value}')
            print(f'EXP:{expected_value}')
            assert check_value == expected_value, f'Значение поля {field_name_2} не найдено в JSON-ответе'
            print(type(check_value))

    @staticmethod
    def get_json_field_value(result, field_name_1, index, field_name_2):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1][field_name_2][index]  # Получаем объект с заданным индексом
        print(f'Значение из объекта #{index + 1} в массиве "{field_name_1}" в поле "{field_name_2}": {field_value}')
        return field_value

    # уровень вложенности 3
    @staticmethod
    def check_json_value_3(result, field_name_1, field_name_2, field_name_3, expected_value):
        check = result.json()  # видим ответ в виде json строки
        check_value = check.get(field_name_1, {}).get(field_name_2, {}).get(
            field_name_3)  # получаем значение определенного поля из ответа
        print(f'Значение проверяемого поля {field_name_3}: {check_value}')
        assert check_value == expected_value
        print("JSON response field PASSED")

    """Метод проверки искомого значения в полях"""

    @staticmethod
    def check_json_value_searched(result, field_name_1, field_name_2, value_searched):
        check = result.json()  # выводим ответ в виде json строки
        check_value = check.get(field_name_1, {}).get(field_name_2)  # получаем значение определенного поля из ответа
        print(f'Поиск осуществляется в поле "{field_name_2}" в значении "{check_value}"')
        if value_searched in check_value:
            print(f'Искомое значение "{value_searched}" присутствует! PASSED')
        else:
            raise AssertionError(f'Искомое значение НЕ найдено! FAILED')

    @staticmethod
    def check_json_value_searched_1(result, field_name_1, value_searched):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1]
        if value_searched in field_value:
            print(f'Искомое значение "{value_searched}" присутствует! PASSED')
        else:
            raise AssertionError(f'Искомое значение НЕ найдено! FAILED')


    """Метод получения значения из вложенного поля в ответе"""

    @staticmethod
    def get_json_value(result, field_name_1, field_name_2):
        check = result.json()  # выводим ответ в виде json строки
        check_value = check.get(field_name_1, {}).get(field_name_2)  # получаем значение определенного поля из ответа
        print(f'Полученное значение из поля {field_name_2}: {check_value}')
        return check_value

    """Сравнение значений"""

    @staticmethod # сравнения двух значений
    def assert_values(expected_value, result_value):
        assert expected_value == result_value, "Значения не равны"
        print("Сравниваемые значения равны")

    @staticmethod
    def assert_value_less(result, expected_value):
        assert result < expected_value, "Сравнение значений не пройдено"
        print(f'Сравнение значений успешно')

# class Validate(BaseModel):
#     """Валидация JSON полей в ответе NFT каталога"""
#     id: int
#     name: (int, float, str)
#     description: str
#     price: (int, float)
#     price_usd: (int, float)
#     price_usd_sale: (int, float)
#     sale: (int, float)
#     picture: str
#     video: str
#     created_at: str
#     updated_at: str
#
#     def validate_catalog_nft_json(self, result):
#         try:
#             # Преобразуйте JSON-ответ в объект Python
#             result_data = json.loads(result)
#             if "data" in result_data:
#                 # Проверьте каждый элемент в списке "data", тут же провалились в массив data
#                 for item_data in result_data["data"]:
#                     nft_item = NftCatalogJSON(**item_data) #распаковка словаря из ответа json и передача его как аргумента
#                     print(f'JSON содержит верные {nft_item}')
#             else:
#                 print("JSON does not contain the 'data' field.")
#         except json.JSONDecodeError as e:
#             print(f"Invalid JSON: {e}")
#         # except ValidationError as e:
#         #     print(f"JSON does not match the expected schema: {e}")
