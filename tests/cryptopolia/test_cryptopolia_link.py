import pytest
from pages.login_page import LoginPage
from config_check import *
from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters
from utilities.utilities import Instruments


@pytest.fixture
def register_with_email():
    email = Instruments.generate_unique_email()  # генерация уникального email
    result_reg = Dexart_api.register_with_mail(email, ref=None, partner_slug=None)
    # проверка статус кода
    Checking.check_status_code(result_reg, 200)
    yield email
    # here could be user deleting steps


class TestCryptopoliaLink:

    @staticmethod
    def check_cryptopolia_user(auth_token, uuid):
        result = Dexart_api.cryptopolia_user(auth_token)
        Checking.check_status_code(result, 200)
        cryptopolia_id = Getters.get_json_field_value_2(result, "data", "uuid")
        assert cryptopolia_id == uuid, "Wrong Cryptopolia UUID"

    @pytest.mark.prod
    def test_set_cryptopolia_link_on_register(self, browser_page):
        cryptopolia_link = "?group=Cryptopolia&uuid="
        uuid = "387665745"
        # generate a new unique email
        email = Instruments.generate_unique_email()
        # open browser from fixture
        page = browser_page
        # register with method from Login page
        lp = LoginPage(page, BASE_URL + cryptopolia_link + uuid)
        lp.email_register(email, "1qazXSW@")
        lp.assert_auth(email)
        # check that page reloaded for authorized user
        page.locator("span[class='headerText headerText_assets']").wait_for()
        # check that my user become a Cryptopolist
        auth_token = Getters.get_cookie_value(page, "accountToken")
        self.check_cryptopolia_user(auth_token=auth_token, uuid=uuid)

    @pytest.mark.prod
    def test_set_cryptopolia_link_on_login(self, register_with_email, browser_page):
        cryptopolia_link = "?group=Cryptopolia&uuid="
        uuid = "387665745"
        # register first
        email = register_with_email
        page = browser_page
        # then auth
        lp = LoginPage(page, BASE_URL + cryptopolia_link + uuid)
        lp.email_login(email, "1qazXSW@")

        # assert auth
        lp.assert_auth(email)
        # check that my user become a Cryptopolist

        auth_token = Getters.get_cookie_value(page, "accountToken")
        self.check_cryptopolia_user(auth_token=auth_token, uuid=uuid)

    @pytest.mark.prod  # check with user oton, it's the same as other drivers
    def test_set_cryptopolia_being_authed(self, register_with_email, browser_page):
        cryptopolia_link = "?group=Cryptopolia&uuid="
        uuid = "387665745"
        # register first
        email = register_with_email
        page = browser_page
        # then auth
        lp = LoginPage(page, BASE_URL)
        lp.email_login(email, "1qazXSW@")
        lp.assert_auth(email)
        # go by cryptopolia link
        page.goto(BASE_URL + cryptopolia_link + uuid)

        # check that my user become a Cryptopolist
        auth_token = Getters.get_cookie_value(page, "accountToken")
        self.check_cryptopolia_user(auth_token=auth_token, uuid=uuid)

    # check ref data priority
    # def test_priority_ref_links(self, browser_page):
    #     cryptopolia_link = "?group=Cryptopolia&uuid="
    #     uuid = "387665745"
    #
    #
    #
    #     page = browser_page
    #     page.goto(BASE_URL + cryptopolia_link + uuid)
