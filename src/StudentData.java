import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public final class StudentData {
    public static final List<String> HEADER = List.of("name", "ID", "gender");

    private StudentData() { }

    public static Path defaultInput() {
        Path canonical = Path.of("StudentData.csv");
        return Files.exists(canonical) ? canonical : Path.of("Ex3StudentData.csv");
    }

    public static ArrayList<Student> read(Path file) throws IOException {
        ArrayList<List<String>> rows = Csv.read(file);
        if (rows.isEmpty() || rows.get(0).size() != HEADER.size()) {
            throw new IOException("Expected CSV header: name,ID,gender in " + file);
        }
        for (int i = 0; i < HEADER.size(); i++) {
            if (!HEADER.get(i).equalsIgnoreCase(rows.get(0).get(i).trim())) {
                throw new IOException("Expected CSV header: name,ID,gender in " + file);
            }
        }
        ArrayList<Student> students = new ArrayList<>();
        for (int i = 1; i < rows.size(); i++) {
            List<String> row = rows.get(i);
            if (row.size() == 1 && row.get(0).isBlank()) {
                continue;
            }
            if (row.size() != 3) {
                throw new IOException("Expected three fields in student record " + (i + 1));
            }
            try {
                students.add(new Student(row.get(0), row.get(1), row.get(2)));
            } catch (IllegalArgumentException exception) {
                throw new IOException("Invalid student record " + (i + 1) + ": "
                        + exception.getMessage(), exception);
            }
        }
        return students;
    }

    public static ArrayList<Student> input(Scanner scanner, int count) {
        ArrayList<Student> students = new ArrayList<>();
        for (int i = 1; i <= count; i++) {
            System.out.println("Student " + i + " of " + count);
            String name = ConsoleInput.readRequired(scanner, "Name: ");
            String id = ConsoleInput.readRequired(scanner, "ID: ");
            String gender = ConsoleInput.readRequired(scanner, "Gender: ");
            students.add(new Student(name, id, gender));
        }
        return students;
    }

    public static void write(Path file, List<Student> students) throws IOException {
        ArrayList<List<String>> rows = new ArrayList<>();
        rows.add(HEADER);
        for (Student student : students) {
            rows.add(student.toRow());
        }
        Csv.write(file, rows);
    }
}
