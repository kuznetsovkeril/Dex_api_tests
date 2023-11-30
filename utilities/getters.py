import json

from utilities.api import Dexart_api

"""Методы получения необходимых данных из JSON"""


class Getters():

    @staticmethod  # поиск конкретных данных из ответа json с множеством объектов, например,нужно найти какое-то поле у юзера для nft с id 48
    # этот метод пока не использовался, но может
    def get_field_value_among_objects(result, field_name_1, field_name_2, searched_value, field_name_3):
        data = json.load(result.text)
        for item in data[field_name_1]:
            if item[field_name_2] == searched_value:
                result_value = item[field_name_3]
                print(f'Искомое значение {result_value}')
                return result_value
            else:
                print(f'Искомое значение не найдено')

    @staticmethod  # простое получение значения из поля без вложений
    def get_json_field_value_0(result, field_name_1):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1]
        print(f'Значение в поле "{field_name_1}": {field_value}')
        return field_value

    @staticmethod  # получаем поле с множеством объектов на втором уровне вложенности
    def get_json_field_value(result, field_name_1, field_name_2, index, field_name_3):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1][field_name_2][index][field_name_3]
        print(f'Значение из объекта #{index + 1} в поле "{field_name_3}": {field_value}')
        return field_value

    @staticmethod  # простое получение значения поля на втором уровне вложенности
    def get_json_field_value_2(result, field_name_1, field_name_2):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1][field_name_2]
        print(f'Значение в поле "{field_name_2}": {field_value}')
        return field_value

    @staticmethod
    def get_json_field_value_3(result, field_name_1, field_name_2, field_name_3):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1][field_name_2][field_name_3]
        print(f'Значение в поле "{field_name_3}": {field_value}')
        return field_value

    @staticmethod
    def get_json_field_value_4(result, field_name_1, field_name_2, field_name_3, field_name_4):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1][field_name_2][field_name_3][field_name_4]
        print(f'Значение в поле "{field_name_4}": {field_value}')
        return field_value

    @staticmethod  # получение значения поля с вложенными объектами в первом уровне
    def get_object_json_field_value(result, field_name_1, index, field_name_2):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1][index][field_name_2]  # Получаем объект с заданным индексом
        print(f'Значение из объекта #{index + 1} в массиве "{field_name_1}" в поле "{field_name_2}": {field_value}')
        return field_value

    @staticmethod  # поиск парселя по статусу и ценовой зоне в конкретном районе
    def get_parcel_by_status(result, status_id, price_zone):
        parsed_json_data = json.loads(result.text)
        free_parcel_id = None
        # ищет объект (item) в массиве дата по условию, что его поля будут иметь соответствующее значение
        for item in parsed_json_data["data"]:
            if item["status_id"] == status_id and item["price_zone"] == price_zone:
                free_parcel_id = item["id"]
                print(f'Свободный парсель найден: {free_parcel_id}')
                break
        # условие если парсель будет найден
        if free_parcel_id is not None:
            return free_parcel_id
        else:
            raise ValueError("Парсел с заданными параметрами не найден")
        # выводим сообщение, если ничего не найдено

    @staticmethod
    def get_user_parcels(result):
        result_json = json.loads(result.text)
        parcels_list = []
        for item in result_json["data"]:
            for parcel in item["parcels"]:
                parcels_list.append(parcel["id"])
        print(parcels_list)
        return parcels_list

    @staticmethod  # метод получения значения поля из множества объектов на третьем уровне вложенности
    def get_object_json_field_value_3(result, field_name_1, index, field_name_2, field_name_3):
        json_response = json.loads(result.text)
        field_value = json_response[field_name_1][index][field_name_2][
            field_name_3]  # Получаем объект с заданным индексом
        print(f'Значение из объекта #{index + 1} в поле "{field_name_2}.{field_name_3}": {field_value}')
        return field_value

    @staticmethod
    def get_order_dxa_amount(order_id):
        result = Dexart_api.check_order(order_id)
        dxa_amount = Getters.get_json_field_value_2(result, "data", "dxa_amount")
        dxa_amount_float = float(dxa_amount.replace(",", ""))
        return dxa_amount_float

    @staticmethod
    def get_dexart_transaction_by_order_id(auth_token, order_id):
        result = Dexart_api.user_transaction(auth_token)
        data = json.loads(result.text)

        for item in data["data"]:
            if order_id in item["description"]:
                print(f'Order id was found in {item}')
                transaction_id = item["id"]
                return transaction_id
            else:
                raise ValueError("Order id was not found!")

    """Method for UI tests"""

    @staticmethod
    def get_cookie_value(page, cookie_name):
        cookies = page.context.cookies()
        print(cookies)
        for cookie in cookies:
            if cookie["name"] == cookie_name:
                cookie_value = cookie["value"]
                print(f'Cookie "{cookie_name}" = "{cookie_value}"')
                return cookie_value
        else:
            raise ValueError("Cookie not found")
