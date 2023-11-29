import pytest

from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters


class TestRentRooms:

    @staticmethod
    def register_with_email(email):
        result = Dexart_api.register_with_mail(email=email, ref=1462487975, partner_slug=None)
        Checking.check_status_code(result, 400)
        message = Getters.get_json_field_value_0(result, "message")
        return message

    """Check notification while register users with different drivers"""

    @pytest.mark.parametrize("email, driver, test_name",
                             [("nikolajkorzovatyh9@gmail.com", "Google", "Test Google account exists"),
                              ("dhmnvjnbn7@privaterelay.appleid.com", "Apple", "Test Google account exists")])
    def test_notification_with_password(self, email, driver, test_name):
        actual_message = self.register_with_email(email=email)
        expected_message = f"You already have an account with {driver} login, use it to log in."
        assert actual_message == expected_message, "Wrong notification"
