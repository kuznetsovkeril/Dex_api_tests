import json
import time

import pytest

from pages.dexart_balance_page import DexartBalancePage
from pages.dexart_referral_page import DexartReferralPage
from pages.office_marketplaces_page import OfficeMarketplacesPage
from utilities.api import Dexart_api
from utilities.checking import Checking
from utilities.getters import Getters
from config_check import *


class TestRentRooms:

    @staticmethod
    def get_free_room_date(room_name):
        result = Dexart_api.get_events_calendar(room_name)
        Checking.check_status_code(result, 200)
        data = json.loads(result.text)

        free_time = None
        for item in data["data"]:
            if item["is_free"] is True:
                free_time = item["time"]
                break

        if free_time is not None:
            pass
        else:
            print("No free time slots")

        free_time_valid = free_time[:-3]

        return free_time_valid

    @staticmethod
    def get_room_data(room_name):
        result = Dexart_api.get_spaces_list()
        Checking.check_status_code(result, 200)
        data = json.loads(result.text)

        rent_price = None
        commission = None
        for item in data["data"]:
            if item["name"] == room_name:
                rent_price = item["room_rental_price"]
                commission = item["dexart_commission"]
                break
        return rent_price, float(commission)

    @staticmethod
    def rent_room(auth_token, date, room_name):
        result = Dexart_api.book_room(auth_token, date, room_name)
        Checking.check_status_code(result, 201)
        order_id = Getters.get_json_field_value_2(result, "data", "id")
        return str(order_id)

    @staticmethod
    def get_owner_payment_amount(auth_token, order_id):
        transaction_id = Getters.get_dexart_transaction_by_order_id(auth_token=auth_token, order_id=order_id)
        print(transaction_id)
        result = Dexart_api.get_transaction_by_id(transaction_id=transaction_id)
        transaction_amount = Getters.get_json_field_value_2(result, "data", "amount")
        return float(transaction_amount)

    # check amount of the room owner payment with different rooms params
    @pytest.mark.parametrize("auth_token, room_name, owner_auth, ref_commission, test_name",
                             [(AUTH_KIRTEST, "room_with_ref_com", AUTH_ROOM_OWNER, 35,
                               "Test owner payment with ref and commission for rent"),
                              (AUTH_KIRTEST, "room_with_no_ref_com", AUTH_ROOM_OWNER, 0,
                               "Test owner payment without ref but commission for rent"),
                              (AUTH_KIRTEST, "room_with_ref_no_com", AUTH_ROOM_OWNER, 35,
                               "Test owner payment without commission but ref for rent"),
                              (AUTH_KIRTEST, "room_with_no_ref_no_com", AUTH_ROOM_OWNER, 0,
                               "Test owner payment without ref and commission for rent")
                              ])
    def test_room_owner_payment(self, auth_token, room_name, owner_auth, ref_commission, test_name):

        # get free date for rent room
        date = self.get_free_room_date(room_name=room_name)

        # book this date and get order id
        order_id = self.rent_room(auth_token=auth_token, date=date, room_name=room_name)

        time.sleep(3)

        # get owner payment with commission and ref
        actual_owner_payment = self.get_owner_payment_amount(auth_token=owner_auth, order_id=order_id)

        # calculate expected amount of owner payment
        rent_price, commission = self.get_room_data(room_name=room_name)

        expected_owner_payment = rent_price - (rent_price * (commission + ref_commission) / 100)

        # assertion
        assert expected_owner_payment == actual_owner_payment, "Wrong owner payment"

    @pytest.mark.parametrize("auth_token, room_name, office_url, test_name",
                             [(AUTH_ATON_USER, "room_with_ref_com", "https://aton-dev.108dev.ru",
                               "Test accrual for rent in ATON"),
                              (AUTH_SPACAD_USER, "room_with_ref_no_com", "https://spacad-dev.108dev.ru",
                               "Test accrual for rent in SPACAD"),
                              (AUTH_UP2U_USER_WALLET, "room_with_ref_com", "https://up-dev.108dev.ru",
                               "Test accrual for rent in UP2U")])
    def test_accruals_for_rent_in_partners(self, auth_token, room_name, office_url, test_name):
        date = self.get_free_room_date(room_name=room_name)
        order_id = self.rent_room(auth_token=auth_token, date=date, room_name=room_name)

        time.sleep(3)

        OfficeMarketplacesPage.search_order_in_partners_marketplaces(base_url=office_url, order_id=order_id)

    @pytest.mark.parametrize("auth_token, room_name, oton_auth, test_name",
                             [(AUTH_OTON_USER, "room_with_ref_com", USER_DEXART_OTON_AUTH,
                               "Test accrual for rent in OTON")])
    def test_accruals_for_rent_in_oton(self, auth_token, room_name, oton_auth, test_name):
        date = self.get_free_room_date(room_name=room_name)
        order_id = self.rent_room(auth_token=auth_token, date=date, room_name=room_name)

        time.sleep(3)

        OfficeMarketplacesPage.search_order_in_oton_marketplaces(oton_auth=oton_auth, order_id=order_id)

    @pytest.mark.parametrize("auth_token, room_name, sponsor_auth, test_name",
                             [(AUTH_DEXART_REF, "room_with_ref_com", AUTH_DEXART_SPONSOR,
                               "Test accrual for rent in OTON")])
    def test_accruals_for_rent_in_dexart(self, auth_token, room_name, sponsor_auth, test_name):

        date = self.get_free_room_date(room_name=room_name)
        order_id = self.rent_room(auth_token=auth_token, date=date, room_name=room_name)

        # get dxa amount
        dxa_amount = Getters.get_order_dxa_amount(order_id=order_id)

        # get sponsor's ref percent
        ref_percent = DexartReferralPage.get_sponsor_percent(AUTH_DEXART_SPONSOR)

        # check transaction in daxart (amount)

        time.sleep(3)

        # get last transaction amount
        transaction_amount = DexartBalancePage.get_last_transaction_amount(AUTH_DEXART_SPONSOR)

        # assertion
        expected_amount = dxa_amount * ref_percent / 100
        print(expected_amount)
        assert expected_amount == transaction_amount, "Wrong transaction amount!"


