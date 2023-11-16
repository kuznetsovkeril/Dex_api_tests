import re
import time

import pytest
from playwright.sync_api import expect

from config_check import *

from pages.login_page import LoginPage


class TestEnergyUnitsPage:

    """Tests link to Energy units landing and its working"""

    # test Get Energy UNITS button, that it is available for all users

    @pytest.mark.parametrize("auth_token, test_name", [
        (AUTH_DEXART_WALLET, "Test EU for Low zone parcel"),
        (AUTH_GOOGLE_ATON, "Test google aton"),
        (AUTH_OTON_USER, "Test oton"),
        (AUTH_SPACAD_USER, "Test spacad email"),
        (AUTH_APPLE_USER_DEX, "Test apple user")])
    def test_get_energy_units_button(self, browser_page, auth_token, test_name):
        page = browser_page
        lp = LoginPage(page, BASE_URL)
        lp.login_with_cookie(auth_token)

        page.goto(BASE_URL + "/balance")
        page.get_by_role("link", name="Parcels").click()
        page.get_by_role("button", name="Your Energy Units are now at the Factory").click()
        page.get_by_role("link", name="Get Energy UNITS").click()
        with page.expect_popup() as page1_info:
            page.get_by_role("link", name="Get Energy UNITS").click()
        page1 = page1_info.value
        expect(page1).to_have_title("DEXART Metaverse Tokens Staking")

    def test_set_email_and_auth_on_landing(self):
        # data saved in cookies
        # I see my mail in form
        # the email is disabled
        # check order
        pass

    def test_go_direct_link_to_landing(self):
        pass