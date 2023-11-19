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
    def test_set_email_on_landing(self, browser_page):
        email = "test@fexbox.org"
        # open browser and login
        page = browser_page
        lp = LoginPage(page, BASE_URL)
        lp.email_login(email=email, password="1qazXSW@")

        # get auth token

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
        page1.click('div[class="packagesBox__plusMinus"]')
        # click button buy -> the form opened
        page1.get_by_role("button", name="Buy").click()

        # assertions
        # 1) check if the email is set in email input
        time.sleep(1)
        # get value email field with JavaScript
        email_input_vale = page1.evaluate('''() => {
        const input = document.querySelector('input[type="email"]');
        return input ? input.value : null;
    }''')
        print(email_input_vale)
        assert email_input_vale == email

        # 2) auth is set
        page1.on("request", lambda request: print(">>", request.method, request.url))

    # check the auth token routed in order energy request
    def test_set_auth_on_landing(self, browser_page):
        page = browser_page
        page.goto(f'{BASE_ENERGY_URL}/?email=kirtest@fexbox.org&token={AUTH_KIRTEST}')
        page.get_by_role("button", name="Accept Cookies").click()

        # accept cookies
        page.get_by_role("button", name="Accept Cookies").click()
        # pick up first package
        page.click('div[class="packagesBox__plusMinus"]')
        # click button buy -> the form opened
        page.get_by_role("button", name="Buy").click()
        # pay modal opens
        page.get_by_text("Choose payment method").click()
        page.get_by_text("Crypto wallet").click()
        page.locator("label").click()
        page.get_by_role("dialog").get_by_role("button", name="Buy").click()

        # get auth header value in the order request
        with page.expect_request("https://stacking-api.108dev.space/api/orders") as response_info:
            page.get_by_role("dialog").get_by_role("button", name="Buy").click()
        request = response_info.value
        header_value = request.header_value("authorization")
        # assert request header with auth token
        assert header_value == f'Bearer {AUTH_KIRTEST}'

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

    def test_go_to_direct_energy_link(self, browser_page):
        page = browser_page
        page.goto(BASE_ENERGY_URL)
        page.get_by_role("button", name="Accept Cookies").click()
        # check if the purchase is not available
        page.get_by_role("heading", name="Energy Units sale is over").is_visible()
