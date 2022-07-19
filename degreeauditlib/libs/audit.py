import logging
import sqlite3
from sqlite3 import Cursor

from degreeauditlib.libs.requirements.base import load_requirements

"""
Home of the Auditor class.
"""


class Auditor:
    """
    The Auditor class creates and executes a query which indicates the status of student(s) degree progress.
    """

    def __init__(self, cur: Cursor, degree_requirements_file: str, student_filter: str = None):
        """
        Initializes the object
        :param cur: Cursor used to execute queries against database
        :param degree_requirements_file:  Path to the requirement JSON file
        :param student_filter: criteria for filtering data from students table (not grades)
        """
        self.__query_begin = 'select "student id", "name", "last term", "total credits", \n'
        self.__query_end_base = 'from students'
        self.__query_end_optional = f' where {student_filter}' if student_filter else ''

        requirements = load_requirements(degree_requirements_file)
        self.query_parts = [req.sql() for req in requirements.gather_requirements()]
        self.cur = cur

    @property
    def query_begin(self):
        return self.__query_begin

    @property
    def query_end(self) -> str:
        return self.__query_end_base + self.__query_end_optional

    @property
    def query(self) -> str:
        return f'{self.query_begin}{", ".join(self.query_parts)}\n{self.query_end}'

    def run_audit(self) -> list[dict]:
        """
        Runs the generated SQL query and returns a list of dictionaries, each dictionary is a row of data.
        :return: Results for each student in a list
        """
        logging.debug(self.query)
        try:
            results = []
            for row in self.cur.execute(self.query):
                results.append(dict(row))
            return results
        except sqlite3.OperationalError as oe:
            logging.error(oe)
            logging.error(self.query)
            raise
