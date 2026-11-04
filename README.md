# PDI Lab 4 - File I/O in Java

Seven exercises and the bonus, completed in separate commits.
Source files, scripts, tests, and code examples contain no comments or docstrings.

## Build and run

Use JDK 17 or newer. No external Java libraries are required.

```powershell
New-Item -ItemType Directory -Force build | Out-Null
javac -encoding UTF-8 -d build src/*.java
```

| Exercise | Command | Result |
| --- | --- | --- |
| 1 | `java -cp build Exercise1` | Save and display 500 random numbers in `LuckyNumber.csv`. |
| 2 | `java -cp build Exercise2` | Create n files in `Ex2LuckyNumber`, then find minimum and maximum. |
| 3 | `java -cp build Exercise3` | Enter three students and save `Ex3StudentData.csv`. |
| 4 | `java -cp build Exercise4` | Read students into an ArrayList and display them. |
| 5 | `java -cp build Exercise5` | Add three students, sort by name, and save `StudentData.csv`. |
| 6 | `java -cp build Exercise6 --summary` | Analyze candidate totals, gender, scores, and groups. |
| 7 | `java -cp build Exercise7 --summary` | Export group CSVs with total and gender summaries. |
| Bonus | `java -cp build BonusExercise` | Serialize and deserialize Student objects as CSV. |

Exercises 1 and 2 use random integers from 1 through 100. Exercise 2 writes
500 values per file. Exercises 4 and 5 use `StudentData.csv` when present,
otherwise `Ex3StudentData.csv`. Student IDs remain text; CSV supports commas,
escaped quotes, multiline fields, and UTF-8.

Place the supplied candidate dataset at `data/CandidatePerformanceTest.csv`.
It stays local and is excluded from Git. Exercises 6 and 7 display records when
`--summary` is omitted. Percentages use each displayed population as the
denominator. Exercise 7 also exports group E, preserving all 958 candidates;
generated group files stay under the ignored `groups/` directory.

## Verify

```powershell
python tests/verify.py
```

The checks always run with fictional data and additionally verify the original
dataset when it is available locally. The script accepts `--java` and `--dataset`.

## Report

[Lab report](output/pdf/Lab4_Report.pdf) uses plain portrait pages, black
headings, pseudocode, flowcharts, CodeSnap RS images, and text output.
Demonstration students are fictional. Student identity fields are left blank.

Install the Windows VSIX from
[anupheap/codesnap-rs-vscode](https://github.com/anupheap/codesnap-rs-vscode).
The report images use the renderer from that installed VS Code adapter.
The workspace settings enable filenames and source line numbers.

To rebuild the report, also install Python packages `reportlab` and `Pillow`,
and use Node.js:

```powershell
python scripts/capture_runs.py
node scripts/capture_codesnap.cjs
python scripts/build_report.py
```

`capture_runs.py` accepts `--java`. Set `CODESNAP_EXTENSION_PATH` if the
adapter is installed outside the standard VS Code extensions directory.
`build_report.py` accepts `--student-name`, `--student-id`, and `--class-group`
for a personal copy. The report evidence is stored once in `output/report/`.
