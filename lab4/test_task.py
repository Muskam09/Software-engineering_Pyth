import pytest

from lab4.task import reverse_string


@pytest.mark.parametrize(
    "current_string, reversed_str",
    [
        pytest.param("abcd efgh",
                     "dcba hgfe",
                     id="revers_without_number_or_symbol"
                     ),
        pytest.param("a1bcd efg!h",
                     "d1cba hgf!e",
                     id="revers_with_number_or_symbol"
                     ),
        pytest.param("",
                     "",
                     id="revers_empty_string"
                     ),
        pytest.param("          ",
                     "          ",
                     id="revers_with_only_spaces_string"
                     )

    ]
)
def test_get_human_age(current_string: str, reversed_str: str) -> None:
    assert reverse_string(current_string) == reversed_str


