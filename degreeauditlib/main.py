import logging
import sys

from sqlite3 import Cursor

from degreeauditlib.libs.audit import Auditor
from degreeauditlib.libs.database import create_db_connection, create_cursor, create_tables


# TODO: Add Sentry or Rollbar

# from libs.requirements.base import verify_json_file


def setup(data_file: str, database: str = ':memory:') -> Cursor:
    """
    Performs basic setup of the underlying database.
    :param data_file: NetStride data file in Excel format
    :param database: File path or :memory: for an in-memory database
    :return: Cursor to the database
    """
    conn = create_db_connection(database)
    cur = create_cursor(conn)
    create_tables(conn, data_file)

    return cur


def main(cur: Cursor, requirements_file: str):
    audit = Auditor(cur, degree_requirements_file=requirements_file)
    for rec in audit.run_audit():
        print(rec)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename="../logs/main.log",
                        encoding='utf-8',
                        level=logging.DEBUG)
    logging.info('Started')
    cursor = setup('../degree-students(3).xlsx', ':memory:')

    main(cursor, sys.argv[1])

    logging.info('Finished')
