import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class BonusExercise {
    public static void serialize(List<Student> students, Path file) throws IOException {
        StudentData.write(file, students);
    }

    public static ArrayList<Student> deserialize(Path file) throws IOException {
        return StudentData.read(file);
    }

    public static void main(String[] args) throws IOException {
        Path input = args.length > 0 ? Path.of(args[0]) : StudentData.defaultInput();
        Path output = args.length > 1 ? Path.of(args[1]) : Path.of("BonusStudents.csv");
        ArrayList<Student> original = StudentData.read(input);
        serialize(original, output);
        System.out.println("Serialized " + original.size() + " Student objects to " + output);
        ArrayList<Student> restored = deserialize(output);
        System.out.println("Deserialized " + restored.size() + " Student objects:");
        for (Student student : restored) {
            System.out.println(student);
        }
        if (!original.equals(restored)) {
            throw new IllegalStateException("CSV round-trip verification failed.");
        }
        System.out.println("Round-trip verified: every restored object equals its original.");
    }
}
