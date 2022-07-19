from degreeauditlib.libs.requirements.base import ProgramRequirement


def test_gather_requirements():
    prog_req = ProgramRequirement(**{"name": "Testing",
                                     "required_courses": ["RP 500", "RP 504"],
                                     "min_electives": 2,
                                     "one_c": True,
                                     "multi_c": True,
                                     "required_electives": ["RP 600", "RP 699"],
                                     "min_600_level_electives": 2})

    reqs = prog_req.gather_requirements()

    is_list = isinstance(reqs, list)
    every_element_is_strategy = True
    is_sql_str = True

    for i in reqs:
        if 'merge_program_requirements' in i.__dict__ and 'sql' in i.__dict__:
            every_element_is_strategy = False
            break
        if not isinstance(i.sql(), str):
            is_sql_str = False
            break

    assert is_list and every_element_is_strategy and is_sql_str
