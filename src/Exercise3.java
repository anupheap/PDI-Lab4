import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Scanner;

public class Exercise3 {
    public static void main(String[] args) throws IOException {
        Scanner scanner = new Scanner(System.in, StandardCharsets.UTF_8);
        ArrayList<Student> students = StudentData.input(scanner, 3);
        Path file = Path.of("Ex3StudentData.csv");
        StudentData.write(file, students);
        System.out.println("Saved " + students.size() + " students to " + file);
    }
}
