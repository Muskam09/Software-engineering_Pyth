import pytest
from typing import Any

from lab5.task5 import converts_amount_into_written_amount, get_hryvnia_form, get_kopeck_form


@pytest.mark.parametrize(
    "amount, result",
    [
        (0, "Нуль гривень 0 копійок"),
        (4.01, "Чотири гривні 1 копійка"),
        (201.42, "Двісті одна гривня 42 копійки"),
        (1.42, "Одна гривня 42 копійки")

    ]
)
def test_converts_amount_into_written_amount(amount: float | int, result: str) -> None:
    assert converts_amount_into_written_amount(amount) == result


@pytest.mark.parametrize(
    "decimal,excepted_error",
    [
        ("100500", TypeError),
        (-100500, ValueError),
        (1005000, ValueError)
    ]
)
def test_convert_decimal_to_words_error(decimal: Any, excepted_error: Exception) -> None:
    with pytest.raises(excepted_error):
        converts_amount_into_written_amount(decimal)
