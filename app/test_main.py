import pytest
from app.main import get_human_age   # adjust import if needed

@pytest.mark.parametrize(
    "cat_age,dog_age,expected",
    [
        (0, 0, [0, 0]),          # both zero
        (14, 14, [0, 0]),        # just below first threshold
        (15, 15, [1, 1]),        # exactly first threshold
        (23, 23, [1, 1]),        # just below second threshold
        (24, 24, [2, 2]),        # exactly second threshold
        (27, 27, [2, 2]),        # within plateau
        (28, 28, [3, 2]),        # cat crosses next boundary
        (100, 100, [21, 17]),    # large values
    ]
)
def test_examples(cat_age, dog_age, expected):
    assert get_human_age(cat_age, dog_age) == expected


def test_cat_boundaries():
    # 15 cat years → 1 human
    assert get_human_age(15, 0)[0] == 1
    # 24 cat years → 2 human
    assert get_human_age(24, 0)[0] == 2
    # 28 cat years → 3 human
    assert get_human_age(28, 0)[0] == 3


def test_dog_boundaries():
    # 15 dog years → 1 human
    assert get_human_age(0, 15)[1] == 1
    # 24 dog years → 2 human
    assert get_human_age(0, 24)[1] == 2
    # 29 dog years → 3 human
    assert get_human_age(0, 29)[1] == 3


@pytest.mark.parametrize(
    "cat_age,dog_age",
    [
        (16, 20),
        (30, 35),
        (50, 60),
    ]
)
def test_monotonic_increase(cat_age, dog_age):
    """Ensure human age never decreases as pet age increases."""
    prev = get_human_age(cat_age - 1, dog_age - 1)
    curr = get_human_age(cat_age, dog_age)
    assert curr[0] >= prev[0]
    assert curr[1] >= prev[1]
