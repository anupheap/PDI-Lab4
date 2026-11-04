import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public final class StudentData {
    public static final List<String> HEADER = List.of("name", "ID", "gender");

    private StudentData() { }

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
