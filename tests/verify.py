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


with tempfile.TemporaryDirectory(prefix="pdi-lab4-") as directory:
    work = pathlib.Path(directory)
    output = run("Exercise1", work)
    with (work / "LuckyNumber.csv").open(encoding="utf-8", newline="") as stream:
        numbers = [int(row[0]) for row in csv.reader(stream)]
    assert len(numbers) == 500 and all(1 <= n <= 100 for n in numbers)
    displayed = re.findall(r"\d+", output.split("Reading them back:\n")[1].split("Numbers read:")[0])
    assert list(map(int, displayed)) == numbers
    print("PASS Exercise 1: 500 saved numbers match the displayed file contents")
