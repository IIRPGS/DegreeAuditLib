import logging
import sqlite3
from sqlite3 import Cursor, Connection

import pandas as pd
from pandas import Series, DataFrame

"""
All of the SQLite functions (and some Pandas data manipulation). 
"""


def create_table(conn: sqlite3.Connection, data: pd.DataFrame, table_name: str):
    """
    Creates a table with a specified table name and containing the specified data from a dataframe object.
    :param conn: Connection to the SQLite database
    :param data: Data to populate the new table
    :param table_name: Name of the new table
    :return: None
    """
    row_count = data.to_sql(table_name, conn)

    logging.info(f'Created table {table_name} added: {row_count} records')


def create_grade_data(all_data: DataFrame) -> DataFrame:
    """
    Creates a new dataframe that is a relational representation of the students' courses and grades.
    :param all_data: Dataframe that houses the student data, with course grade information
    :return: Dataframe with student id, grade, course, section information
    """

    logging.info("Creating grade information dataframe")

    raw_courses = all_data.loc[:, ['Course Graded', ]]
    raw_courses['Course Graded'] = raw_courses['Course Graded'].str.rstrip(', ')
    course_grades = raw_courses['Course Graded'].str.split(', ', expand=True).apply(Series, 1).stack()
    course_grades.index = course_grades.index.droplevel(-1)
    course_grades.name = 'CourseGrade'
    course_grade_sections = course_grades.str.split(': ', expand=True)
    course_grade_sections.columns = ['Course', 'Grade']
    course_grades = course_grade_sections['Course'].str.split(".", expand=True)
    course_grade_sections['Course'], course_grade_sections['Section'] = course_grades[0], course_grades[1]

    logging.info("Finished grade information dataframe")

    return course_grade_sections


def create_db_connection(database_file: str = ':memory:') -> Connection:
    """
    Creates a database connection to a SQLite database,
    connection's row factory returns a dictionary of column name and value.
    :param database_file: string path to the database file
    :return: Connection to the SQLite database.
    """
    logging.info("Creating database connection")

    conn = sqlite3.connect(database_file)
    conn.row_factory = sqlite3.Row

    logging.info("Finished database connection")
    return conn


def create_cursor(conn: Connection) -> Cursor:
    """
    Creates a cursor for a connection.
    :param conn: Connection to database
    :return: Cursor connected to the connection
    """
    cur = conn.cursor()
    return cur


# noinspection PyArgumentList
def create_tables(conn: Connection, excel_file: str,
                  student_columns=['Name', 'Last Term', 'Total Credits', 'Course in Progress', ]) -> None:
    """
    Creates the tables students and grades in the SQLite database.
    :param conn: Connection to database
    :param excel_file: NetStride data file
    :param student_columns: Column names to be included in creating the student table
    :return: None
    """
    all_data = pd.read_excel(excel_file, index_col=14)
    create_table(conn, all_data.loc[:, student_columns], 'students')
    create_table(conn, create_grade_data(all_data), 'grades')
