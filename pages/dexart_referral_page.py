from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters


class DexartReferralPage:

    @staticmethod
    def get_sponsor_percent(auth_token):
        result = Dexart_api.user_referral_info(auth_token)
        Checking.check_status_code(result, 200)
        ref_percent = Getters.get_json_field_value_2(result, "data", "percent")
        return ref_percent
