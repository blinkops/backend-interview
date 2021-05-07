import pytest

from app import SHORT_DATA_PATH
from handlers.db import init_db


def test_init_db_success():
    db = init_db(path=SHORT_DATA_PATH)
    assert db


def test_init_db_failed():
    with pytest.raises(TypeError):
        _ = init_db(path=None)
