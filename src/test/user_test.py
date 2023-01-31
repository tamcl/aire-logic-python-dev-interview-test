import logging
import os
from urllib.parse import urljoin
from uuid import uuid4

import pytest
import requests
from pydantic import ValidationError

from src.database.models.users import User

BASE_URL = "http://0.0.0.0:80/"


def user_test_case_1():
    user1 = dict(username="hello", email="hello@example.com")
    # with pytest.raises(ValidationError):
    User(**user1)
    return user1


def user_test_case_2():
    user2 = dict(username="hello2", email="Not an Email")
    with pytest.raises(ValueError):
        User(**user2)
    return user2


def user_test_case_3():
    user3 = dict(username="hello3", email="hello3@example.com")
    # with pytest.raises(ValidationError):
    User(**user3)
    return user3


def user_test_case_4():
    user4 = dict(username="hello4", email="hello4@example.com")
    User(**user4)
    return user4


def test_create_user_1():
    logging.info("test_create_user_1")
    user = dict(username="jakesmith001", email="jakesmith@example.com")
    return requests.post(os.path.join(BASE_URL, "user/"), json=user).json()


def test_create_user_2():
    logging.info("test_create_user_2")
    user = dict(username="jakesmith002", email="jakesmith2@example.com")
    return requests.post(os.path.join(BASE_URL, "user/"), json=user).json()


def test_get_user_1():
    logging.info("test_get_user_1")
    username = "jakesmith001"
    return requests.get(os.path.join(BASE_URL, f"user/{username}")).json()


def test_get_user_2():
    logging.info("test_get_user_2")
    username = "jakesmith002"
    return requests.get(os.path.join(BASE_URL, f"user/{username}")).json()


def test_update_username():
    logging.info("test_update_username")
    username = "jakesmith_update"
    update_username = dict(username="jakesmith001", email="jakesmith@example.com")
    return requests.post(
        os.path.join(BASE_URL, f"user/update/?newUsername={username}"),
        json=update_username,
    ).json()


def user_test():
    logging.info("Test validator")
    user_test_case_1()
    user_test_case_2()
    user_test_case_3()
    user_test_case_4()

    logging.info("Test user functions")
    logging.info(test_create_user_1())
    logging.info(test_create_user_2())
    logging.info(test_get_user_1())
    logging.info(test_get_user_2())
    logging.info(test_update_username())
