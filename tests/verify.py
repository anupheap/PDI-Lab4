"""Integration checks. Compile src/*.java first; run with Python 3.10+."""
import argparse
import csv
import collections
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--java", default="java")
parser.add_argument("--dataset", type=pathlib.Path, default=ROOT / "data" / "CandidatePerformanceTest.csv")
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

    def summary(title, rows):
        male = sum(row[1].lower() == "male" for row in rows)
        female = len(rows) - male
        percent = lambda n: 100 * n / len(rows) if rows else 0
        return (f"{title}\nTotal candidates: {len(rows)}\n"
                f"Male candidates: {male} ({percent(male):.2f}%)\n"
                f"Female candidates: {female} ({percent(female):.2f}%)")

    def check_analysis(file, candidates):
        output = run("Exercise6", work, "", str(file), "--summary")
        assert summary("All candidates", candidates) in output
        qualified = [row for row in candidates if float(row[9]) >= 90]
        assert summary("Average score >= 90", qualified) in output
        for column, name in [(5, "Math"), (6, "English"), (7, "Computer")]:
            count = sum(float(row[column]) >= 85 for row in candidates)
            assert f"{name} score >= 85: {count}\n" in output
        count = sum(all(float(row[i]) >= 85 for i in (5, 6, 7)) for row in candidates)
        assert f"All three subjects >= 85: {count}\n" in output
        groups = collections.defaultdict(list)
        for row in candidates:
            groups[row[2]].append(row)
        for group, members in groups.items():
            assert summary(group.title(), members) in output
        return output

    header = ["ID", "gender", "group", "Education", "test preparation\ncourse",
              "Math", "English", "Computer", "Total", "Average"]
    title = ["List of candidates with the test scores", *([""] * 9)]
    dataset = args.dataset.resolve()
    if dataset.exists():
        with dataset.open(encoding="utf-8-sig", newline="") as stream:
            original = list(csv.reader(stream))
        index = next(i for i, row in enumerate(original) if row and row[0] == "ID")
        candidates = [row for row in original[index + 1:] if any(row)]
        check_analysis(dataset, candidates)
        print(f"PASS original local dataset: {len(candidates)} candidates (not published)")
    else:
        print("SKIP original dataset: local CSV not provided; fictional fixture checks still run")

    boundary = work / "boundaries.csv"
    fixture = []
    for i, (gender, group, scores, average) in enumerate([
            ("male", "A", (90, 90, 90), "90"),
            ("female", "A", (89, 90, 90), "89.67"),
            ("female", "B", (85, 85, 85), "85"),
            ("male", "E", (100, 100, 100), "100"),
            ("female", "D", (84, 85, 86), "85"),
            ("male", "C", (0, 0, 0), "0")], 1):
        fixture.append([str(i), gender, f"group {group}", "college, test", 'a "quote"',
                        *map(str, scores), str(sum(scores)), average])
    with boundary.open("w", encoding="utf-8-sig", newline="") as stream:
        csv.writer(stream).writerows([title, header, *fixture])
    check_analysis(boundary, fixture)
    empty = work / "empty.csv"
    with empty.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream).writerow(header)
    assert "NaN" not in check_analysis(empty, [])
    assert "college, test" in run("Exercise6", work, "", str(boundary))
    print("PASS Exercise 6: threshold boundaries, groups, display, and empty populations")

    def check_exports(file, source, label):
        folder = work / label
        output = run("Exercise7", work, "", str(file), str(folder), "--summary")
        expected_groups = {"A", "B", "C", "D"} | {row[2].split()[-1] for row in source}
        assert {p.name for p in folder.glob("*.csv")} == {f"group{g}.csv" for g in expected_groups}
        exported = []
        for group in expected_groups:
            with (folder / f"group{group}.csv").open(encoding="utf-8", newline="") as stream:
                rows = list(csv.reader(stream))
            members = [row for row in source if row[2] == f"group {group}"]
            assert len(rows[0]) == 10 and all(len(row) == 10 for row in rows)
            assert rows[1:-3] == members
            assert rows[-3][:2] == ["Summary - total students", str(len(members))]
            for index, gender in [(-2, "male"), (-1, "female")]:
                count = sum(row[1] == gender for row in members)
                percent = 100 * count / len(members) if members else 0
                assert rows[index][:2] == [f"Summary - {gender} (%)", f"{percent:.2f}%"]
            exported.extend(rows[1:-3])
        assert collections.Counter(map(tuple, exported)) == collections.Counter(map(tuple, source))
        assert f"Exported {len(source)} candidates to {len(expected_groups)} group files." in output

    check_exports(boundary, fixture, "fixture-groups")
    check_exports(empty, [], "empty-groups")
    if dataset.exists():
        check_exports(dataset, candidates, "original-groups")
    print("PASS Exercise 7: all groups, lossless partition, rectangular CSV, footer statistics, empty groups")
