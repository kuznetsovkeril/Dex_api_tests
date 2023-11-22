from utilities.api import Dexart_api
from utilities.getters import Getters


class DexartOrderPage:

    @staticmethod
    def get_odred_dxa_amount(order_id):
        result = Dexart_api.check_order(order_id)
        dxa_amount = Getters.get_json_field_value_2(result, "data", "dxa_amount")
        return float(dxa_amount)
