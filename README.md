# PDI Lab 4 - File I/O in Java

Solutions to the seven exercises and bonus in the supplied lab handout.
Each exercise is completed in its own commit, in assignment order.

## Requirements and compilation

Use JDK 17 or newer. No external Java libraries are required.
Run commands from the repository root:

```powershell
New-Item -ItemType Directory -Force build | Out-Null
javac -encoding UTF-8 -d build src/*.java
```

## Exercise 1

```powershell
java -cp build Exercise1
```

Generates exactly 500 random integers, writes `LuckyNumber.csv`, then reads
the file back and displays every number. Since this exercise does not specify
a range, it uses 1 through 100, inclusive, consistent with exercise 2.
Generated files are UTF-8 and are excluded from version control.

## Exercise 2

```powershell
java -cp build Exercise2
```

Prompts for a positive file count `n`, creates `Ex2LuckyNumber/file1.csv`
through `filen.csv`, reads their numbers into an `ArrayList<Integer>`, and
prints the minimum and maximum. The handout does not specify the number of
values per file; this solution uses 500 per file, each from 1 through 100.
Only files created by the current run are read, so older extra files do not
affect the result.

## Verification

After compilation, run `python tests/verify.py`. The tests use temporary
working folders under `tmp/` and do not replace your exercise output files.

## Exercise 3

```powershell
java -cp build Exercise3
```

Enter the name, ID, and gender of each of three team members when prompted.
The program writes `Ex3StudentData.csv` with a header. IDs remain text so
leading zeroes are preserved. CSV fields containing commas or quotes are
escaped correctly. The report uses clearly labeled fictional demonstration
students; enter your actual team members when running the program.

## Exercise 4

```powershell
java -cp build Exercise4
# Or specify a CSV explicitly:
java -cp build Exercise4 Ex3StudentData.csv
```

Reads students into an `ArrayList<Student>` and displays them. The handout
calls exercise 3's file both `Ex3StudentData.csv` and `StudentData.csv`.
To make the exercises work in sequence, exercise 4 reads `StudentData.csv`
when it exists, otherwise `Ex3StudentData.csv`. An explicit path overrides this.

## Exercise 5

```powershell
java -cp build Exercise5
# Optional input and output paths:
java -cp build Exercise5 Ex3StudentData.csv StudentData.csv
```

Loads the existing students using the same filename fallback as exercise 4,
prompts for three more students, sorts by name A-Z ignoring case, then saves
`StudentData.csv` and displays the sorted list. The first default run has six
students. Later runs append three to the current `StudentData.csv`.
