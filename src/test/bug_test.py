import logging
import os

import requests

from src.database.models.bugs import Bug

BASE_URL = "http://0.0.0.0:80/"


def create_bug_test_1(userid):
    bug_details = dict(
        title="This is the first bug of the testing",
        description="This will test if the creation of the bug is successful",
        createdBy=userid,
    )
    return requests.post(os.path.join(BASE_URL, f"bug/"), json=bug_details).json()


def create_bug_test_2(userid):
    bug_details = dict(
        title="bug test 2",
        description="API login end point validation latency ",
        createdBy=userid,
    )
    return requests.post(os.path.join(BASE_URL, "bug/"), json=bug_details).json()


def create_bug_test_3(userid):
    bug_details = dict(title="bug test 3", description="should fail", createdBy=userid,)
    return requests.post(os.path.join(BASE_URL, "bug/"), json=bug_details).json()

def create_bug_test_4():
    bug_details = dict(title="bug test 3", description="should fail because of the createdby", createdBy="fail")
    return requests.post(os.path.join(BASE_URL, "bug/"), json=bug_details).json()


def assign_bug_test_1(bugid, userid):
    url_param = dict(bugid=bugid, userid=userid)
    return requests.post(os.path.join(BASE_URL, "bug/assign/"), params=url_param).json()


def assign_bug_test_2(bugid, userid):
    url_param = dict(bugid=bugid, userid=userid)
    return requests.post(os.path.join(BASE_URL, "bug/assign/"), params=url_param).json()


def close_bug_test_1(bugid):
    url_param = dict(bugid=bugid)
    return requests.post(os.path.join(BASE_URL, "bug/close/"), params=url_param).json()


def view_bug_list_test(status):
    url_param = dict(status=status)
    return requests.get(os.path.join(BASE_URL, "bug/list/"), params=url_param).json()


def view_bug_test_1(bug_id):
    url_param = dict(bugid=bug_id)
    return requests.get(os.path.join(BASE_URL, "bug/"), params=url_param).json()


def bug_test(userid_1, userid_2):
    logging.info("Create test")
    create_bug_test_1_results = create_bug_test_1(userid_1)
    logging.info(create_bug_test_1_results)
    bug_id_1 = create_bug_test_1_results.get("uuid")
    create_bug_test_2_results = create_bug_test_2(userid_2)
    logging.info(create_bug_test_2_results)
    bug_id_2 = create_bug_test_2_results.get("uuid")
    logging.info(create_bug_test_3(userid_1))
    logging.info(create_bug_test_4())

    logging.info("Assign test")
    logging.info(assign_bug_test_1(bug_id_1, userid_2))
    logging.info(assign_bug_test_2(bug_id_2, "NOSUCHID"))

    logging.info("Close test")
    close_bug_test_1(bug_id_1)

    logging.info("View list test")
    logging.info(view_bug_list_test("any"))
    logging.info(view_bug_list_test("open"))
    logging.info(view_bug_list_test("close"))

    logging.info("View bug test")
    logging.info(view_bug_test_1(bug_id_1))
