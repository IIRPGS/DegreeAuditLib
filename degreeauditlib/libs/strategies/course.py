import json


class CourseStrategy:
    """
    The strategy for required courses.
    """
    def __init__(self, file: str, required_courses):
        with open(file, 'r') as fp:
            info = json.load(fp)
        self.name: str = info['name']

        self.required_courses = required_courses

        self.base_query: str = info['query']

    def merge_program_requirements(self):
        query_parts = []
        for r in self.required_courses:
            query_parts.append(self.base_query.format(r=r))
        return ", \n".join(query_parts)

    def sql(self):
        return self.merge_program_requirements()
