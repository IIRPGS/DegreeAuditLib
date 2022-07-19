from pathlib import Path

import pytest

from degreeauditlib.libs.requirements.base import verify_json_file


def test_verify_json_file_success():
    file = 'GCRP.json'
    assert isinstance(verify_json_file(file), Path)


def test_verify_json_file_failure():
    file = 'tests/does_not_exist'
    with pytest.raises(FileNotFoundError):
        _ = verify_json_file(file)
