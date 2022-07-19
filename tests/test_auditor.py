import sqlite3
from pathlib import Path
from sqlite3 import Cursor, Connection

import pandas as pd
import pytest
from pytest import fixture

from degreeauditlib.libs.database import create_table
from degreeauditlib.libs.audit import Auditor


@fixture
def database() -> Connection:
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row

    df = pd.DataFrame([(12116, 'RP 500', 'A', '01'),
                       (12116, 'RP 506', 'A', '01'),
                       (12116, 'RP 525', 'A', '02'),
                       (12116, 'RP 550', 'A-', '02'),
                       (12116, 'RP 610', 'A-', '01'),
                       (12116, 'RP 622', 'A', '01'),
                       (12116, 'RP 623', 'A', '01'),
                       (12116, 'RP 652', 'A', '01'),
                       (12116, 'RP 662', 'A', '01')],
                      columns=['Student ID', 'Course', 'Grade', 'Section'])
    df.set_index('Student ID')

    create_table(conn, df, 'Grades')

    df = pd.DataFrame([(12116, 'Joe Schmoe', 'Spring 2022', '27'), ],
                      columns=['Student ID', 'Name', 'Last Term', 'Total Credits', ])
    df.set_index('Student ID')

    create_table(conn, df, 'Students')

    return conn


@fixture
def cursor(database) -> Cursor:
    return database.cursor()


def test_auditor_success(cursor):
    audit = Auditor(cursor, 'GCRP.json', student_filter='"Student ID" in (12116)')
    assert audit.run_audit() == [{"'RP 500','RP 504'": 'True',
                                  "'RP 525'": 'True',
                                  'Last Term': 'Spring 2022',
                                  'MinElectivesStrategy': 'True',
                                  'MultiCStrategy': 'True',
                                  'Name': 'Joe Schmoe',
                                  'OneCStrategy': 'True',
                                  'Student ID': 12116,
                                  'Total Credits': '27'}]


def test_auditor_failure(cursor):
    audit = Auditor(cursor, 'GCRP.json', student_filter='where f = 100')
    with pytest.raises(sqlite3.OperationalError) as e_info:
        audit.run_audit()
