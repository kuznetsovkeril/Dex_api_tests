import time

from config_check import *

from utilities.getters import Getters


class LoginPage:

    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def email_login(self, email, password):
        self.page.goto(self.base_url)
        self.page.get_by_role("button", name="Let’s go").click()
        self.page.get_by_label("Enter your email").fill(email)
        self.page.keyboard.press('Enter')
        self.page.get_by_label("Password").fill(password)
        self.page.keyboard.press('Enter')
        time.sleep(4)
        # check that auth executed correctly
        account_email = Getters.get_cookie_value(self.page, "accountEmail")
        assert account_email == email, "Wrong account email"

    def email_register(self, email, password):
        self.page.goto(self.base_url)
        self.page.get_by_role("button", name="Let’s go").click()
        self.page.get_by_label("Enter your email").fill(email)
        self.page.keyboard.press('Enter')
        self.page.get_by_label("Password").fill(password)
        self.page.locator("label").filter(
            has_text="I understand and agree to the Terms of Sale, Privacy Policy and Rules and Guidel").get_by_role(
            "img").click()
        self.page.get_by_label("Password").press("Enter")
        time.sleep(3)
        account_email = Getters.get_cookie_value(self.page, "accountEmail")
        assert account_email == email, "Wrong account email"

    def login_with_cookie(self, cookie_value):
        self.page.goto(self.base_url)
        self.page.context.add_cookies([{"name": "accountToken", "value": cookie_value, "url": self.base_url}])
        self.page.reload()

    # impossible due to privacy
    def google_login(self):
        pass

    # impossible due to captcha
    def oton_login(self):
        pass

    # impossible due to extension
    def wallet_login(self):
        pass
