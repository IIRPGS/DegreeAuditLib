import sqlite3
from sqlite3 import Connection, Cursor

import pandas as pd

from degreeauditlib.libs.database import create_table, create_db_connection, create_cursor, create_tables

conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row


def test_create_db_connection():
    test_conn = create_db_connection()
    assert isinstance(test_conn, Connection)


def test_create_cursor():
    test_conn = create_db_connection()
    test_cur = create_cursor(test_conn)
    assert isinstance(test_cur, Cursor)


def test_create_tables():
    conn = create_db_connection()
    create_tables(conn, 'sample_data.xlsx')

    cur = create_cursor(conn)
    result = cur.execute("select count() from students").fetchone()
    assert result[0] > 0


def test_load_grades():
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

    cur = conn.cursor()
    result = cur.execute('select count() from grades').fetchone()

    assert result[0] == df.count(0)[0]


def test_load_students():
    df = pd.DataFrame([(12116, 'Joe Schmoe', 'Spring 2022', '27'), ],
                      columns=['Student ID', 'Name', 'Last Term', 'Total Credits', ])
    df.set_index('Student ID')

    create_table(conn, df, 'Students')

    cur = conn.cursor()
    result = cur.execute('select count() from students').fetchone()

    assert result[0] == df.count(0)[0]
