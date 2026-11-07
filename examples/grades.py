"""成績の共通契約。順位は丸めていない合計点で決める。"""

from collections.abc import Mapping
from math import isfinite

SUBJECTS = frozenset({"国語", "英語", "数学"})


def validate_scores(scores):
    if not isinstance(scores, Mapping) or set(scores) != SUBJECTS:
        raise ValueError("scoresには国語・英語・数学の3科目を指定してください")
    for value in scores.values():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("点数にはbool以外の数値を指定してください")
        if not isfinite(value) or not 0 <= value <= 100:
            raise ValueError("点数は有限の0～100で指定してください")
    return scores


def calculate_total(scores):
    return sum(validate_scores(scores).values())


def calculate_average(scores):
    return calculate_total(scores) / 3


def get_grade(average):
    if isinstance(average, bool) or not isinstance(average, (int, float)):
        raise ValueError("平均点にはbool以外の数値を指定してください")
    if not isfinite(average) or not 0 <= average <= 100:
        raise ValueError("平均点は有限の0～100で指定してください")
    return "合格" if average >= 60 else "不合格"


def rank_students(students):
    if not isinstance(students, list):
        raise ValueError("studentsにはリストを指定してください")
    rows = []
    for student in students:
        if not isinstance(student, Mapping):
            raise ValueError("各生徒はオブジェクトで指定してください")
        name = student.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("生徒名を指定してください")
        total = calculate_total(student.get("scores"))
        average = total / 3
        rows.append({"name": name.strip(), "scores": dict(student["scores"]),
                     "total": total, "average": average, "grade": get_grade(average)})
    rows.sort(key=lambda row: row["total"], reverse=True)
    previous = None
    rank = 0
    for index, row in enumerate(rows, 1):
        if previous is None or row["total"] != previous:
            rank = index
        previous = row["total"]
        row["rank"] = rank
    return rows
