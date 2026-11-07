import copy

import pytest

from examples import calculator as calc, grades


def scores(value):
    return {subject: value for subject in grades.SUBJECTS}


def test_calculator_arithmetic_and_zero_division():
    assert [calc.add(2, 3), calc.subtract(2, 3), calc.multiply(2, 3), calc.divide(2, 4)] == [5, -1, 6, .5]
    with pytest.raises(ZeroDivisionError, match="ゼロでは除算できません"):
        calc.divide(1, 0)


@pytest.mark.parametrize("value", [True, "5", None, float("nan"), float("inf")])
def test_calculator_rejects_invalid_input(value):
    with pytest.raises(ValueError):
        calc.add(value, 1)


def test_competition_ranking_is_stable_and_does_not_mutate():
    students = [{"name": name, "scores": scores(value)} for name, value in [("山田花子", 80), ("佐藤健", 80), ("鈴木葵", 59)]]
    before = copy.deepcopy(students)
    rows = grades.rank_students(students)
    assert [row["rank"] for row in rows] == [1, 1, 3]
    assert [row["name"] for row in rows] == ["山田花子", "佐藤健", "鈴木葵"]
    assert rows[0]["total"] == 240
    assert rows[2]["grade"] == "不合格"
    assert students == before
    assert grades.rank_students([]) == []
    assert grades.get_grade(60) == "合格"


@pytest.mark.parametrize("bad", [None, {}, {"国語": 90}, {**scores(90), "体育": 80}, scores(True), scores(-1), scores(101), scores(float("nan")), scores("90")])
def test_scores_validation(bad):
    with pytest.raises(ValueError):
        grades.calculate_total(bad)


def test_unrounded_ranking():
    rows = grades.rank_students([
        {"name": "山田花子", "scores": scores(80.001)},
        {"name": "佐藤健", "scores": scores(80.002)},
    ])
    assert [row["rank"] for row in rows] == [1, 2]
    assert rows[0]["name"] == "佐藤健"
