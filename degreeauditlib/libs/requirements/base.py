import importlib.metadata
import importlib.resources as res
from importlib.resources import files
import json
import os.path
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from degreeauditlib.libs.strategies.min_electives import MinElectivesStrategy
from degreeauditlib.libs.strategies.course import CourseStrategy
from degreeauditlib.libs.strategies.multi_c_strategy import MultiCStrategy
from degreeauditlib.libs.strategies.one_c_strategy import OneCStrategy
from degreeauditlib.libs.strategies.six_hundred_level_electives import Min600LevelElectivesStrategy

"""
Requirements.base provides functionality to load requirements and configure the list of strategies to be deployed. 
"""


class ProgramRequirement(BaseModel):
    name: str
    required_courses: Optional[list[str]]
    min_electives: Optional[int]
    one_c: Optional[bool]
    multi_c: Optional[bool]
    required_electives: Optional[list[str]]
    min_600_level_electives: Optional[int]

    def gather_requirements(self, working_directory: str = r'./') -> list:
        """
        Pulls the strategies from the requirements fields to include only the
        strategies that are needed for the program (degree, certificate, etc.).
        :return: A list of strategies that make up the program requirement.
        """

        # To add a strategy, the key must match what is in the requirements file.
        # The strategy class must exist and any parameters must exist be assigned to the same key from the requirements
        # file with _params at the end of the name.
        requirement_lookup = {"required_courses": CourseStrategy,
                              "required_courses_params": [files('degreeauditlib.strategy').joinpath('course_strategy.json').resolve(),
                                                          self.required_courses],
                              "min_electives": MinElectivesStrategy,
                              "min_electives_params": [files('degreeauditlib.strategy').joinpath('min_electives_strategy.json').resolve(),
                                                       self.required_courses,
                                                       self.min_electives],
                              "one_c": OneCStrategy,
                              "one_c_params": [files('degreeauditlib.strategy').joinpath('one_c_strategy.json').resolve()],
                              "multi_c": MultiCStrategy,
                              "multi_c_params": [files('degreeauditlib.strategy').joinpath('multi_c_strategy.json').resolve()],
                              "required_electives": CourseStrategy,
                              "required_electives_params": [files('degreeauditlib.strategy').joinpath('course_strategy.json').resolve(),
                                                            self.required_electives],
                              "min_600_level_electives": Min600LevelElectivesStrategy,
                              "min_600_level_electives_params": [
                                  files('degreeauditlib.strategy').joinpath('six_hundred_level_electives.json').resolve(),
                                  self.required_courses, self.min_600_level_electives]
                              }

        requirements = []
        for attr in self.__dict__:
            # Only appending the requirement if the requirement exists in the requirement_lookup and has a value.
            if attr in requirement_lookup and self.__dict__[attr]:
                # Creating the object of the classes provided in the requirement_lookup.
                requirements.append(requirement_lookup[attr](*requirement_lookup[f"{attr}_params"]))
        return requirements


def load_requirements(file: str) -> ProgramRequirement:
    """
    Loads the requirements from a JSON file that then creates a ProgramRequirement object.
    :param file:
    :return: The configuration of a program requirement.
    """
    if not file.endswith('.json'):
        file = file + '.json'

    res_files = [resource.name for resource in files('degreeauditlib.requirement').iterdir() if resource.is_file()]
    if file not in res_files:
        verify_json_file(file)

    json_file = files('degreeauditlib.requirement').joinpath(file).open('r')
    programs_raw = json.load(json_file)
    return ProgramRequirement(**programs_raw)


def verify_json_file(file_path: str) -> Path:
    """
    Verifies that the file exists and ends with a json extension.
    :param file_path: str object that points to a file
    :return: Path object if the file does exist.
    """
    if not file_path.endswith('.json'):
        file_path = file_path + '.json'
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return Path(file_path)
    raise FileNotFoundError(f"{file_path} either does not exist, is not a file, or is in a different folder")
