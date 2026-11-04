"""Capture genuine program runs for the lab report without publishing candidate rows."""
import argparse
import collections
import csv
import json
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--java", default="java")
options = parser.parse_args()
evidence = ROOT / "output" / "report" / "evidence"
evidence.mkdir(parents=True, exist_ok=True)
(ROOT / "tmp").mkdir(exist_ok=True)
dataset = ROOT / "data" / "CandidatePerformanceTest.csv"

titles = {
    "Exercise1": ("Exercise 1 - Lucky numbers", "Generate, save, and reread 500 integers."),
    "Exercise2": ("Exercise 2 - Multiple files", "Read 1,500 values from three files into an ArrayList."),
    "Exercise3": ("Exercise 3 - Save students", "Enter three fictional demonstration team members."),
    "Exercise4": ("Exercise 4 - Read students", "Reconstruct students in an ArrayList and display them."),
    "Exercise5": ("Exercise 5 - Add and sort", "Add three demonstration students and save six names in A-Z order."),
    "Exercise6": ("Exercise 6 - Candidate analysis", "Analyze the supplied local dataset; publish aggregate output only."),
    "Exercise7": ("Exercise 7 - Group exports", "Export every group and append total and gender summaries."),
    "BonusExercise": ("Bonus - CSV object round trip", "Serialize Student objects and verify the reconstructed objects."),
}
records = []
with tempfile.TemporaryDirectory(dir=ROOT / "tmp", prefix="report-") as directory:
    work = pathlib.Path(directory)

    def capture(name, stdin="", arguments=(), shown_arguments=()):
        result = subprocess.run(
            [options.java, "-cp", str(ROOT / "build"), name, *map(str, arguments)],
            cwd=work, input=stdin, text=True, encoding="utf-8", capture_output=True,
            check=True, timeout=30,
        )
        if result.stderr:
            raise RuntimeError(result.stderr)
        title, description = titles[name]
        records.append({"class": name, "title": title, "description": description,
                        "command": " ".join(["java -cp build", name, *shown_arguments]),
                        "stdin": stdin, "stdout": result.stdout,
                        "source": f"src/{name}.java"})
        (evidence / f"{name}.txt").write_text(result.stdout.rstrip("\n") + "\n",
                                             encoding="utf-8", newline="\n")

    capture("Exercise1")
    capture("Exercise2", "3\n")
    capture("Exercise3", 'Zoe, Chan\n001\nfemale\nBora "Bo"\n002\nmale\nAna\n003\nfemale\n')
    capture("Exercise4")
    capture("Exercise5", "dara\n006\nmale\nChenda\n005\nfemale\nBopha\n004\nfemale\n")
    capture("Exercise6", arguments=(dataset, "--summary"),
            shown_arguments=("data/CandidatePerformanceTest.csv", "--summary"))
    capture("Exercise7", arguments=(dataset, "groups", "--summary"),
            shown_arguments=("data/CandidatePerformanceTest.csv", "groups", "--summary"))
    capture("BonusExercise")

verification = subprocess.run(
    ["python", str(ROOT / "tests" / "verify.py"), "--java", options.java],
    cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True, timeout=60,
)
(evidence / "verification.txt").write_text(verification.stdout.rstrip("\n") + "\n",
                                          encoding="utf-8", newline="\n")
with dataset.open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.reader(stream))
header_index = next(i for i, row in enumerate(rows) if row and row[0] == "ID")
candidates = [row for row in rows[header_index + 1:] if any(row)]
groups = collections.defaultdict(list)
for row in candidates:
    groups[row[2]].append(row)


def aggregate(label, members):
    male = sum(row[1] == "male" for row in members)
    return {"label": label, "total": len(members), "male": male, "female": len(members) - male}


payload = {"runs": records, "verification": verification.stdout,
           "summary": [aggregate("All candidates", candidates),
                       aggregate("Average >= 90", [row for row in candidates if float(row[9]) >= 90]),
                       *[aggregate(group.title(), members) for group, members in sorted(groups.items())]],
           "source_revision": subprocess.check_output(
               ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()}
(evidence / "runs.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
print(f"Captured {len(records)} successful runs and full verification; no candidate records published.")
