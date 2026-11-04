import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;

/** Loads student objects from CSV into an ArrayList, then displays that list. */
public class Exercise4 {
    public static void main(String[] args) throws IOException {
        Path file = args.length > 0 ? Path.of(args[0]) : StudentData.defaultInput();
        ArrayList<Student> students = StudentData.read(file);
        System.out.println("Loaded " + students.size() + " students from " + file);
        for (Student student : students) {
            System.out.println(student);
        }
    }
}
