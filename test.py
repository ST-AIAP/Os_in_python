import reminder as app
from reminder import Task
import pytest
import datetime as dt


def test_to_date():
    assert app._to_date("2022-09-01") == dt.date(2022, 9, 1)


def test_to_date_exception():
    with pytest.raises(ValueError, match="12345 is not in YYYY-MM-DD format."):
        app._to_date("12345")


@pytest.fixture
def task_list():
    return [Task(name="pay rent"), Task(name="buy bread"), Task(name="buy what")]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("buy bread", Task(name="buy bread")),
        ("buy banana", None),
        ("pay rent", Task(name="pay rent")),
        ("BUY WHAT", Task(name="buy what")),
    ],
)
def test_find_task(test_input, expected, task_list):
    print(test_input)
    assert app._find_task(test_input, task_list) == expected


def test_save_load_task_list(task_list):
    app._save_task_list(task_list)
    load_list = app._get_task_list()
    assert task_list == load_list
