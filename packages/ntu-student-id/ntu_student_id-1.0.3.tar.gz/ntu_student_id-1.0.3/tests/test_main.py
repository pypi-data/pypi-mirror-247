import pytest

from src.main import Parser


def test_parser_full():
    assert Parser("B09902001").full() == "資訊工程學系"


def test_parser_get_by_string():
    assert str(Parser("B09902001")) == "資訊工程學系"


def test_parser_get_all():
    assert Parser("B09902001").all() == {
        "short": "資工系",
        "full": "資訊工程學系",
        "additional": "",
    }


def test_parser_short():
    assert Parser("B09902001").short() == "資工系"


def test_parser_additional():
    assert Parser("B09610001").additional() == "生傳發展系"


def test_parser_invalid_id():
    with pytest.raises(ValueError, match="Invalid Student ID"):
        Parser("B0990200")


def test_parser_invalid_department():
    with pytest.raises(ValueError, match="Invalid Department Code"):
        Parser("B09Y00001")
