import time


class LoginPage:

    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def check_auth(self, email):
        # get all cookies
        cookies = self.page.context.cookies()
        print(cookies)
        for cookie in cookies:
            if cookie["name"] == "accountEmail":
                account_email = cookie["value"]
                print(account_email)
                break
        else:
            raise ValueError("Cookie not found")
        assert email == account_email, "Wrong account email"

    def email_login(self, email, password):
        self.page.goto(self.base_url)
        self.page.get_by_role("button", name="Let’s go").click()
        self.page.get_by_label("Enter your email").fill(email)
        self.page.keyboard.press('Enter')
        self.page.get_by_label("Password").fill(password)
        self.page.keyboard.press('Enter')
        time.sleep(3)
        self.check_auth(email)

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
        self.check_auth(email)

    def google_login(self):
        pass

    def oton_login(self):
        pass

    def wallet_login(self):
        pass

