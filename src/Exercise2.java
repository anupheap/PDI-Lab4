import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;
import java.util.Scanner;

public class Exercise2 {
    private static final int NUMBERS_PER_FILE = 500;

    public static void main(String[] args) throws IOException {
        Scanner scanner = new Scanner(System.in, StandardCharsets.UTF_8);
        int n = ConsoleInput.readPositiveInt(scanner, "Number of files: ");
        Path folder = Path.of("Ex2LuckyNumber");
        Files.createDirectories(folder);
        Random random = new Random();
        for (int i = 1; i <= n; i++) {
            Path file = folder.resolve("file" + i + ".csv");
            try (BufferedWriter writer = Files.newBufferedWriter(file, StandardCharsets.UTF_8)) {
                for (int j = 0; j < NUMBERS_PER_FILE; j++) {
                    writer.write(Integer.toString(random.nextInt(100) + 1));
                    writer.newLine();
                }
            }
        }

        ArrayList<Integer> numbers = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            Path file = folder.resolve("file" + i + ".csv");
            try (BufferedReader reader = Files.newBufferedReader(file, StandardCharsets.UTF_8)) {
                String line;
                while ((line = reader.readLine()) != null) {
                    numbers.add(Integer.parseInt(line));
                }
            }
        }
        System.out.println("Files created: " + n);
        System.out.println("Numbers loaded into ArrayList: " + numbers.size());
        System.out.println("Minimum: " + Collections.min(numbers));
        System.out.println("Maximum: " + Collections.max(numbers));
    }
}
