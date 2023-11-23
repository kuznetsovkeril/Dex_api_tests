import json

from utilities.api import Office_api
from utilities.checking import Checking


class OfficeMarketplacesPage:

    @staticmethod
    def search_order_in_oton_marketplaces(oton_auth, order_id):

        result = Office_api.list_marketplace(auth=oton_auth)
        Checking.check_status_code(result, 200)
        data = json.loads(result.text)

        for item in data["data"]["records"]:
            if order_id in item["product"]:
                print(f'Order id was found in {item}')
                break
        else:
            raise ValueError("Order was not found in Oton marketplaces")

    @staticmethod
    def search_order_in_partners_marketplaces(base_url, order_id):

        result = Office_api.super_table(base_url=base_url, table="marketplace")
        Checking.check_status_code(result, 200)
        # Поиск нужного номера заказа в описании продукта у ATON, SPACAD, UP2U. У OTON такого нет в описании МПЛ
        data = json.loads(result.text)
        for item in data["data"]:
            if order_id in item["product"]:
                print(f'Order id was found in {item}')
                break
        else:
            raise ValueError("Order was not found in partners marketplaces")
