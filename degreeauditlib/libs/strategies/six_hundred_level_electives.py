import json


class Min600LevelElectivesStrategy:
    """
    Number of 600 level electives met (not in the required courses).
    """
    def __init__(self, file: str, required_courses, min_600_level_courses):
        with open(file, 'r') as fp:
            info = json.load(fp)
        self.name: str = info['name']

        self.required_courses = required_courses
        self.min_600_level_courses = min_600_level_courses

        self.base_query: str = info['query']

    def merge_program_requirements(self):
        return self.base_query.format(required_course=", ".join(self.required_courses),
                                      min_600_level_courses=self.min_600_level_courses,
                                      name=self.name)

    def sql(self):
        return self.merge_program_requirements()
