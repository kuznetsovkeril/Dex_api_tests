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
        # open browser and login
        page = browser_page
        lp = LoginPage(page, BASE_URL)
        lp.login_with_cookie(auth_token)

        # open Energy landing
        page.goto(BASE_URL + "/balance")
        page.get_by_role("link", name="Parcels").click()
        page.get_by_role("button", name="Your Energy Units are now at the Factory").click()
        page.get_by_role("link", name="Get Energy UNITS").click()

        # init a new page
        with page.expect_popup() as page1_info:
            page.get_by_role("link", name="Get Energy UNITS").click()
        page1 = page1_info.value
        expect(page1).to_have_title("DEXART Metaverse Tokens Staking")

    # check if
    def test_set_email_and_auth_on_landing(self, browser_page):
        email = "test@fexbox.org"
        # open browser and login
        page = browser_page
        lp = LoginPage(page, BASE_URL)
        lp.email_login(email=email, password="1qazXSW@")

        # go to TPF and go to Energy landing
        page.goto(BASE_URL + "/balance")
        page.get_by_role("link", name="Parcels").click()
        page.get_by_role("button", name="Your Energy Units are now at the Factory").click()
        # init a new page
        with page.expect_popup() as page1_info:
            page.get_by_role("link", name="Get Energy UNITS").click()
        page1 = page1_info.value

        # accept cookies
        page1.get_by_role("button", name="Accept Cookies").click()
        # pick up first package
        page1.locator(".packagesBox__plusMinus").first.click()
        time.sleep(10)
        # click button buy -> the form opened
        page1.get_by_role("button", name="Buy").click()

        # assertions
        time.sleep(1)
        email_input_vale = page1.evaluate('''() => {
        const input = document.querySelector('input[type="email"]');
        return input ? input.value : null;
    }''')
        print(email_input_vale)
        assert email_input_vale == email

    # check if the email input is disabled
    def test_email_input_disabled(self, browser_page):
        page = browser_page
        page.goto(f'{BASE_ENERGY_URL}/?email=kirtest@fexbox.org&token={AUTH_KIRTEST}')
        page.get_by_role("button", name="Accept Cookies").click()

        # also possible code: page.wait_for_selector('div[class="packagesBox__plusMinus"]').click()
        page.click('div[class="packagesBox__plusMinus"]')
        page.get_by_role("button", name="Buy").click()

        # also possible code: assert page.get_by_placeholder("Your email").is_disabled()
        assert page.is_disabled('input[type="email"]')
