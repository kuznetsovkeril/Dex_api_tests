from utilities.api import Nft_api
from utilities.checking import Checking

"""Проверка каталога NFT"""


class Test_get_nft_catalog():

    """Проверка получаемых полей каталога NFT"""

    def test_get_nft_catalog(self):
        print("Get NFT catalog GET request")
        result = Nft_api.nft_catalog("")
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 200)
        # проверка наличия необходимых полей в ответе
        json_fields = ['id', 'name', 'description', 'price', 'price_usd', 'price_usd_sale', 'sale', 'picture', 'video', 'created_at', 'updated_at']
        Checking.check_json_fields_in(result, "data", json_fields)

    def test_search_nft_in_catalog(self):

        """Проверка поиска NFT по имени"""

        print("Get NFT catalog GET request")
        param = "?name=Gravity NFT"
        result = Nft_api.nft_catalog(param)
        # проверка статус кода
        print(f'Фактический статус код: {result.status_code}')
        Checking.check_status_code(result, 200)
        # проверка значения поля name=Gravity NFT
        Checking.check_json_value_v2(result, "data", "name", "Gravity NFT")



