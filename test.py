import logging
import os

from src.database.DBFunctions import (
    query_to_df,
)

from src.test.user_test import user_test
from src.test.bug_test import bug_test


logging.basicConfig(
    format="%(levelname)s: %(asctime)s - %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.info("reseting files")
remove_file = ["./bug_tracker.db"]
for i in remove_file:
    logging.info(f"removing {i}")
    if os.path.basename(i) in os.listdir(os.path.dirname(i)):
        os.remove(i)


user_test()
# logging.info(query_to_df('bug_tracker.db','SELECT * from users').to_dict('records'))
userid_list = list(
    query_to_df("bug_tracker.db", "SELECT uuid from users")
    .to_dict("series")
    .get("uuid")
)
bug_test(*userid_list)
