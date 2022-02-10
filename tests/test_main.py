import pytest
import main


def test_getTop250Tv():
    test_data = main.getTop250Tv()
    assert len(test_data["items"]) == 250


