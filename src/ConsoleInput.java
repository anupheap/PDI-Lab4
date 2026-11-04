import java.util.Scanner;

/** Small shared helpers for interactive lab input. */
public final class ConsoleInput {
    private ConsoleInput() { }

    public static String readRequired(Scanner scanner, String prompt) {
        while (true) {
            System.out.print(prompt);
            if (!scanner.hasNextLine()) {
                throw new IllegalStateException("Input ended before all required values were supplied.");
            }
            String value = scanner.nextLine().trim();
            if (!value.isEmpty()) {
                return value;
            }
            System.out.println("Please enter a non-empty value.");
        }
    }

    public static int readPositiveInt(Scanner scanner, String prompt) {
        while (true) {
            try {
                int value = Integer.parseInt(readRequired(scanner, prompt));
                if (value > 0) {
                    return value;
                }
            } catch (NumberFormatException exception) {
                // Ask again when the input is not an integer.
            }
            System.out.println("Please enter a positive integer.");
        }
    }
}
