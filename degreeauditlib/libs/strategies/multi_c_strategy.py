import json


class MultiCStrategy:
    """
    Multiple C grades received.
    Note: returns False if condition is met to follow the convention of False being an issue.
    """
    def __init__(self, file: str):
        with open(file, 'r') as fp:
            info = json.load(fp)
        self.name: str = info['name']

        self.base_query: str = info['query']

    def merge_program_requirements(self):
        return self.base_query.format(name=self.name)

    def sql(self):
        return self.merge_program_requirements()