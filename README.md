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
