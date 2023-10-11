
import pytest


from utilities.api import Nft_api
from utilities.checking import Checking
from src.auth_tokens import AUTH_DXA_USER

from utilities.utilities import Instruments


class TestNftBuyWithEmail:
    """Проверка покупки NFT с указанием email [DEX-3350]"""

    @pytest.mark.parametrize("pay_driver, payment_link",
                             [("balance", None),
                              ("oton", "https://timbi.org"),
                              ("nearpay", "https://stage-widget.nearpay.co"),
                              ("transak", "https://global-stg.transak.com")])
    def test_buy_nft_with_email(self, pay_driver, payment_link):
        # данные в тело запроса
        pay_method = pay_driver
        nft_id = 48  # Gravity NFT
        amount = Instruments.random_num(3, 10)  # пускай это будет какое-то рандомное число от 3-10, так как для карт мин 15$
        print(f'Покупаемое кол-во NFT: {amount}')
        email = "kirtest@fexbox.org"
        result = Nft_api.buy_nft_with_email(nft_id, amount, pay_method, email)

        # от полученного статус кода зависит по какой логике будет осуществляться проверка
        status_code = result.status_code
        print(f'Полученный статус код: {status_code}')
        if status_code == 401:
            # если 401, проверяю, что получено нужное сообщение в ответе
            expected_message = "Sign in required to use this payment method"
            Checking.check_json_value(result, "message", expected_message)
        elif status_code == 201:
            # если 201, проверяю, что создана ссылка для оплаты
            value_searched = payment_link  # буду проверять, по части ссылок на оплату oton, transak, nearpay
            Checking.check_json_value_searched(result, "data", "payment_url", value_searched)
        else:
            # если придет какой-то другой статус код, тест провален
            raise ValueError("Неверный статус код! Тест FAILED")
