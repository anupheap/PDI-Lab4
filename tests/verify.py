"""Integration checks. Compile src/*.java first; run with Python 3.10+."""
import argparse
import csv
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--java", default="java")
args = parser.parse_args()


def run(name, cwd, stdin="", *arguments):
    result = subprocess.run(
        [args.java, "-cp", str(ROOT / "build"), name, *arguments],
        cwd=cwd, input=stdin, text=True, encoding="utf-8", capture_output=True,
        timeout=30,
    )
    if result.returncode:
        raise AssertionError(f"{name} failed: {result.stdout}\n{result.stderr}")
    return result.stdout


(ROOT / "tmp").mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix="pdi-lab4-", dir=ROOT / "tmp") as directory:
    work = pathlib.Path(directory)
    output = run("Exercise1", work)
    with (work / "LuckyNumber.csv").open(encoding="utf-8", newline="") as stream:
        numbers = [int(row[0]) for row in csv.reader(stream)]
    assert len(numbers) == 500 and all(1 <= n <= 100 for n in numbers)
    displayed = re.findall(r"\d+", output.split("Reading them back:\n")[1].split("Numbers read:")[0])
    assert list(map(int, displayed)) == numbers
    print("PASS Exercise 1: 500 saved numbers match the displayed file contents")

    (work / "Ex2LuckyNumber").mkdir()
    (work / "Ex2LuckyNumber" / "file99.csv").write_text("-999\n", encoding="utf-8")
    output = run("Exercise2", work, "no\n0\n3\n")
    numbers = []
    for i in range(1, 4):
        rows = list(csv.reader((work / "Ex2LuckyNumber" / f"file{i}.csv").open()))
        assert len(rows) == 500
        numbers.extend(int(row[0]) for row in rows)
    assert len(numbers) == 1500 and all(1 <= n <= 100 for n in numbers)
    assert "Numbers loaded into ArrayList: 1500" in output
    assert f"Minimum: {min(numbers)}" in output and f"Maximum: {max(numbers)}" in output
    assert output.count("Please enter a positive integer.") == 2
    print("PASS Exercise 2: file counts, input validation, stale files, and exact extrema")

    students = [["Zoe, Chan", "001", "female"], ["Bora \"Bo\"", "002", "male"],
                ["Ana", "003", "female"]]
    output = run("Exercise3", work, "\n" + "\n".join(v for row in students for v in row) + "\n")
    with (work / "Ex3StudentData.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.reader(stream))
    assert rows == [["name", "ID", "gender"], *students]
    assert "Saved 3 students to Ex3StudentData.csv" in output
    print("PASS Exercise 3: three students, required input, CSV escaping, and leading-zero IDs")

    output = run("Exercise4", work)
    assert "Loaded 3 students from Ex3StudentData.csv" in output
    for name, student_id, gender in students:
        assert f"Name: {name} | ID: {student_id} | Gender: {gender}" in output
    multiline = work / "multiline.csv"
    with multiline.open("w", encoding="utf-8-sig", newline="") as stream:
        csv.writer(stream).writerows([["name", "ID", "gender"], ["Line\nBreak", "004", "female"]])
    assert "Name: Line\nBreak | ID: 004" in run("Exercise4", work, "", str(multiline))
    print("PASS Exercise 4: ArrayList display, file-name fallback, BOM, and multiline fields")

    added = [["dara", "006", "male"], ["Chenda", "005", "female"], ["Bopha", "004", "female"]]
    output = run("Exercise5", work, "\n".join(v for row in added for v in row) + "\n")
    with (work / "StudentData.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.reader(stream))
    expected = sorted(students + added, key=lambda row: (row[0].lower(), row[0], row[1]))
    assert rows == [["name", "ID", "gender"], *expected]
    assert "Saved 6 students sorted by name (A-Z) to StudentData.csv" in output
    assert "Loaded 6 students from StudentData.csv" in run("Exercise4", work)
    assert len(list(csv.reader((work / "Ex3StudentData.csv").open()))) == 4
    print("PASS Exercise 5: append exactly three, sort, save, and reread six students")
