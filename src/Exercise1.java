import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Random;

/** Writes 500 random integers to CSV, then displays the values read from disk. */
public class Exercise1 {
    public static void main(String[] args) throws IOException {
        Path file = Path.of("LuckyNumber.csv");
        Random random = new Random();
        try (BufferedWriter writer = Files.newBufferedWriter(file, StandardCharsets.UTF_8)) {
            for (int i = 0; i < 500; i++) {
                writer.write(Integer.toString(random.nextInt(100) + 1));
                writer.newLine();
            }
        }

        System.out.println("Saved 500 numbers to " + file + ". Reading them back:");
        int count = 0;
        try (BufferedReader reader = Files.newBufferedReader(file, StandardCharsets.UTF_8)) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.printf("%3d%s", Integer.parseInt(line), ++count % 20 == 0 ? "\n" : " ");
            }
        }
        System.out.println("Numbers read: " + count);
    }
}
