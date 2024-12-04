import pytest
from lab6 import selection_sort


@pytest.mark.parametrize(
    "unsorted, sorted",
    [
        ([1, 3, 5, 2, 6, 4], [1, 2, 3, 4, 5, 6]),
        ([12, -16, 13, -10, 20, -11], [-16, -11, -10, 12, 13, 20]),
        ([], []),
        ([5], [5]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([7, 7, 7, 7], [7, 7, 7, 7]),
        ([-3, -1, -7, -5], [-7, -5, -3, -1]),
        ([1.1, 3.3, 2.2, 4.4], [1.1, 2.2, 3.3, 4.4]),
        ([100000, 99999, 100001], [99999, 100000, 100001]),
        ([0, -1, 0, 1], [-1, 0, 0, 1]),
        (["B", "C", "A"], ["A", "B", "C"]),

    ]
)
def test_selection_sort(unsorted: list, sorted: list) -> None:
    assert selection_sort(unsorted) == sorted
