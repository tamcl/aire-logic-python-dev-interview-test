import logging
import requests
import os
from src.database.models.bugs import Bug


BASE_URL = "http://0.0.0.0:80/"

def create_bug_test_1(userid):
    bug_details = dict(
        title='This is the first bug of the testing',
        description='This will test if the creation of the bug is successful',
        createdBy=userid,
    )
    return requests.post(os.path.join(BASE_URL, f'bug/'), json=bug_details)

def create_bug_test_2(userid):
    bug_details = dict(
        title='This is the first bug of the testing',
        description='This will test if the creation of the bug is successful',
        createdBy=userid,
    )
    return requests.post(os.path.join(BASE_URL, f'bug/'), json=bug_details)

def create_bug_test_3(userid):
    bug_details = dict(
        title='This is the first bug of the testing',
        description='This will test if the creation of the bug is successful',
        createdBy=userid,
    )
    return requests.post(os.path.join(BASE_URL, f'bug/'), json=bug_details)

def assign_bug_test_1():
    pass

def assign_bug_test_2():
    pass

def close_bug_test_1():
    pass

def view_bug_list_test_1():
    pass

def view_bug_list_test_2():
    pass

def view_bug_test_1():
    pass

def bug_test(userid_1, userid_2):
    logging.info('Create test')
    create_bug_test_1(userid_1)
    create_bug_test_2(userid_2)
    create_bug_test_3(userid_1)

    logging.info('Assign test')
    assign_bug_test_1()
    assign_bug_test_2()

    logging.info('Close test')
    close_bug_test_1()

    logging.info('View list test')
    view_bug_list_test_1()
    view_bug_list_test_2()

    logging.info('View bug test')
    view_bug_test_1()