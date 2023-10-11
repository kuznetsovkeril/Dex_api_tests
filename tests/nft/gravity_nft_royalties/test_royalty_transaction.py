import json
import time

import pytest

from utilities.api import Dexart_api, Nft_api
from utilities.checking import Checking
from dev_config import AUTH_BUY_GG_ITEMS, AUTH_ONE_GRAVITY_NFT, AUTH_BONUS_NFT, AUTH_KIRTEST, AUTH_NO_GG_NFT
from utilities.getters import Getters
from utilities.utilities import Instruments


class TestRoyaltyTransaction:
    """Проверка расчета транзакции Royalties"""

    # запуск раздачи royalties
    @staticmethod
    def give_royalties():
        result = Dexart_api.give_royalties()
        Checking.check_status_code(result, 200)
        print("Все роялти выданы пользователям")

    # метод покупки booster
    @staticmethod
    def buy_booster(auth, booster_id, room_id):
        result_buy_booster = Dexart_api.buy_booster(auth, booster_id=booster_id, amount=1, room_id=room_id)
        print(f'Room ID: {room_id}')
        Checking.check_status_code(result_buy_booster, 200)
        time.sleep(3)
        print("Бустер успешно куплен")

    @staticmethod
    def refresh_statistic():
        result = Dexart_api.royalties_statistics()
        Checking.check_status_code(result, 200)
        print("Статистика получена и обновлена")
        return result

    @staticmethod
    def get_last_transaction(auth_token, transaction_field):
        result = Dexart_api.user_transaction(auth_token)
        Checking.check_status_code(result, 200)
        field_value = Getters.get_object_json_field_value(result, "data", 0, transaction_field)
        print("Последняя транзакция пользователя получена")
        return field_value

    # получение баланса для конкретной нфт юзера, нам важен gravity nft
    @staticmethod
    def user_nft_balance(auth_token, searched_nft_id):
        result = Nft_api.user_nft_balance(auth_token)
        nft_id = searched_nft_id
        user_nft_balance = None  # инициализация переменной
        data = json.loads(result.text)
        for item in data["data"]:
            if item["catalog_nft_id"] == nft_id:
                user_nft_balance = item["amount"]
                print(f'User NFT id:"{nft_id}", balance is {user_nft_balance}')
                break
            else:
                print(f'Искомый id NFT не был найден на балансе юзера')
        return user_nft_balance

    @staticmethod
    def approximately_assertion_values(expected_value, result_value, tolerance):
        if Instruments.approximately_equal(expected_value, result_value, tolerance):
            print("Юзер получил верное кол-во Gravity NFT royalties")
        else:
            raise ValueError("Получено НЕверное количество royalties!")

    """Проверка, что размер транзакции роялти составляет верное кол-во"""

    @pytest.mark.parametrize("auth_token, test_name", [
        (AUTH_ONE_GRAVITY_NFT, "Testing royalties transaction amount with one Gravity NFT user"),
        (AUTH_BONUS_NFT, "Testing royalties transaction amount with bonus Gravity NFT user"),
        (AUTH_KIRTEST, "Testing royalties transaction amount with all kind of NFT on balance")])
    def test_royalties_transaction_amount(self, auth_token, test_name):
        # получаю статистику и поля из статистики fund_acc и royalty
        statistics = self.refresh_statistic()
        fund_acc = Getters.get_json_field_value_0(statistics, "fund_acc")
        royalty = Getters.get_json_field_value_0(statistics, "royalty")
        total_nfts = Getters.get_json_field_value_0(statistics, "total_nfts")

        # если нет фонда для раздачи роялти
        if fund_acc or royalty <= 0:
            # набиваю fund, чтоб было из чего платить роялти
            self.buy_booster(AUTH_BUY_GG_ITEMS, booster_id=6, room_id="Air Test")

            # получаю новую статистику
            statistics = self.refresh_statistic()
            fund_acc = Getters.get_json_field_value_0(statistics, "fund_acc")
            royalty = Getters.get_json_field_value_0(statistics, "royalty")
            total_nfts = Getters.get_json_field_value_0(statistics, "total_nfts")

        # раздача royalty всем юзерам
        self.give_royalties()

        # получение кол-ва gravity NFT юзера
        user_nft_amount = self.user_nft_balance(auth_token, 48)

        # расчет ожидаемого кол-во роялти для юзера
        sharp_royalty_amount = (user_nft_amount / total_nfts) * fund_acc * 0.15015
        expected_royalty_amount = round(sharp_royalty_amount, 8)
        # проверка, что размер роялти для юзера верное
        time.sleep(3)
        royalty_amount = self.get_last_transaction(auth_token, "amount")
        print(f'Фактическое роялти: {royalty_amount}')
        print(f'Ожидаемое роялти: {expected_royalty_amount}')
        self.approximately_assertion_values(float(expected_royalty_amount), float(royalty_amount), 0.00000009)

    def test_royalties_for_no_nft_owner(self):
        # проверяю, что у юзера точно нет gravity NFT
        user_nft_amount = self.user_nft_balance(AUTH_NO_GG_NFT, 48)
        if user_nft_amount is None:
            # получаю его список транзакций
            user_transaction = Dexart_api.user_transaction(AUTH_NO_GG_NFT)
            # ищу в его транзакциях транзакцию с типом royalty (type_id = 10)
            type_id = 10
            data = json.loads(user_transaction.text)
            for item in data["data"]:
                if item["type"]["id"] == type_id:
                    transaction_id = item["id"]
                    print(f'Транзакция начисления Royalties была найдена. t_id: {transaction_id}')
                    raise ValueError("Ошибка. Найдена транзакция Royalty у юзера без Gravity NFT")
            print(f'Транзакция Royalties НЕ найдена. PASSED.')
        else:
            raise ValueError(f'У юзера есть Gravity NFT на балансе. Тест-кейс некорректен!')
