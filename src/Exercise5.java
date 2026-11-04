import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Scanner;

public class Exercise5 {
    public static void main(String[] args) throws IOException {
        Path input = args.length > 0 ? Path.of(args[0]) : StudentData.defaultInput();
        Path output = args.length > 1 ? Path.of(args[1]) : Path.of("StudentData.csv");
        ArrayList<Student> students = StudentData.read(input);
        System.out.println("Loaded " + students.size() + " students from " + input);
        Scanner scanner = new Scanner(System.in, StandardCharsets.UTF_8);
        students.addAll(StudentData.input(scanner, 3));
        students.sort(Comparator.comparing(Student::name, String.CASE_INSENSITIVE_ORDER)
                .thenComparing(Student::name).thenComparing(Student::id));
        StudentData.write(output, students);
        System.out.println("Saved " + students.size() + " students sorted by name (A-Z) to " + output);
        for (Student student : students) {
            System.out.println(student);
        }
    }
}
