from src.database.models.users import User, User_details
from pydantic import ValidationError
import requests
import os
from urllib.parse import urljoin

import logging
import pytest

BASE_URL = "http://0.0.0.0:80/"


def user_test_case_1():
    user1 = dict(username="hello", email="hello@example.com", password="hello1234")
    with pytest.raises(ValidationError):
        User_details(**user1)

    return user1


def user_test_case_2():
    user2 = dict(username="hello2", email="Not an Email", password="hello2password")
    with pytest.raises(ValueError):
        User_details(**user2)
    return user2


def user_test_case_3():
    user3 = dict(
        username="hello3", email="hello3@example.com", password="wertQWER123@£!@"
    )
    with pytest.raises(ValidationError):
        User_details(**user3)
    return user3


def user_test_case_4():
    user4 = dict(username="hello4", email="hello4@example.com", password="Pass@123")
    User_details(**user4)
    return user4

def test_create_user_1():
    user = dict(username="jakesmith001", email="jakesmith@example.com", password="Pa45tfgbh8tv87v76vg876v8ss@123")
    return requests.post(os.path.join(BASE_URL, 'user/'), json=user).json()

def test_create_user_2():
    user = dict(username="jakesmith001", email="jakesmith@example.com", password="Pass@123")
    return requests.post(os.path.join(BASE_URL, 'user/'), json=User_details(**user).dict()).json()

def test_get_user_1():
    username = "jakesmith001"
    return requests.get(os.path.join(BASE_URL, f'user/{username}')).json()

def test_get_user_2():
    username = "jakesmith002"
    return requests.get(os.path.join(BASE_URL, f'user/{username}')).json()

def test_update_username():
    pass

def test_update_password():
    pass

def test_delete_user():
    pass



def user_test():
    logging.info("Test validator")
    user_test_case_1()
    user_test_case_2()
    user_test_case_3()
    user_test_case_4()

    logging.info("Test user functions")
    print(test_create_user_1())
    print(test_create_user_2())
    print(test_get_user_1())
    print(test_get_user_2())
    test_update_username()
    test_update_password()
    test_delete_user()