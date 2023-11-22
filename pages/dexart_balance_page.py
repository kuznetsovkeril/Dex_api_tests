from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters


class DexartBalancePage:

    @staticmethod
    def get_last_transaction_amount(auth_token):
        result = Dexart_api.user_transaction(auth_token)
        Checking.check_status_code(result, 200)
        transaction_amount = Getters.get_object_json_field_value(result, "data", 0, "amount")
        transaction_amount_float = float(transaction_amount.replace(",", ""))
        return transaction_amount_float

