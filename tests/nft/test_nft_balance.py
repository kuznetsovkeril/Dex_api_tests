from utilities.api import Nft_api
from utilities.checking import Checking
from dev_config import AUTH_DXA_USER
import json
import time

from utilities.utilities import Instruments


class Test_nft_balance:

    """Проверка полей в ответе баланса NFT у юзера"""

    def test_nft_user_balance(self):
        result = Nft_api.user_nft_balance(AUTH_DXA_USER)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 200)
        # проверка наличия необходимых полей в ответе
        fields_name = Checking.show_json_fields_for_item(result, "data",
                                                         0)  # выводим какие поля есть в ответе для одного объекта
        expected_fields = ['id', 'catalog_nft_id', 'catalog_nft', 'user_id', 'transaction', 'amount', 'status', 'order',
                           'status_id', 'created_at']
        Checking.assert_values(fields_name, expected_fields)
        # проверка, что в ответе баланса есть поля с инфой об нфт
        fields_name_nft = Checking.show_json_fields_for_in_item(result, "data", 0, "catalog_nft")
        expected_nft_fields = ['id', 'name', 'description', 'catalog_nft_group_id', 'picture', 'video', 'price',
                               'price_usd', 'sale', 'created_at', 'updated_at']
        Checking.assert_values(expected_nft_fields, fields_name_nft)
        print("В ответе присутствуют все необходимые поля")

    """Проверка, что после покупки баланс нфт меняется"""

    def test_nft_purchase(self):
        # получаем баланс юзера
        result = Nft_api.user_nft_balance(AUTH_DXA_USER)

        # поиск нфт c конкретным id на балансе юзера

        nft_id = 54
        user_nft_balance = None  # инициализация переменной
        data = json.loads(result.text)
        for item in data["data"]:
            if item["catalog_nft_id"] == nft_id:
                user_nft_balance = item["amount"]
                print(f'User NFT id:"{nft_id}", balance is {user_nft_balance}')
                break
            else:
                print(f'Искомый id NFT не был найден на балансе юзера')

        """Проверка, что после покупки изменяется баланс NFT"""

        # покупка NFT
        amount = Instruments.random_num(1, 10)
        print(f'Покупаемое количество NFT: {amount}')
        result_nft_buy = Nft_api.buy_nft(AUTH_DXA_USER, nft_id, amount, pay_method="balance")
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 200)

        time.sleep(5)

        # получаем новый баланс NFT после покупки

        result_new_balance = Nft_api.user_nft_balance(AUTH_DXA_USER)
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 200)

        new_nft_balance = None  # инициализация переменной
        data = json.loads(result_new_balance.text)
        for item in data["data"]:
            if item["catalog_nft_id"] == nft_id:
                new_nft_balance = item["amount"]
                print(f'User NFT id:"{nft_id}", balance after purchase is {new_nft_balance}')
                break
            else:
                print(f'Искомый id NFT не был найден на балансе юзера')

        # новый баланс должен быть такой

        expected_new_nft_balance = user_nft_balance + amount
        print(f'Ожидаемый NFT баланс после покупки: {expected_new_nft_balance}')

        # проверяем, что баланс действительно увеличился на кол-во покупаемых NFT

        Checking.assert_values(expected_new_nft_balance, new_nft_balance)
